# -*- coding: utf-8 -*-
"""
Accuracy Tracker - 准确率追踪与学习系统

该模块提供：
1. 预测记录存储
2. 事后准确率验证
3. 准确率统计计算
4. 趋势分析
5. 准确率告警
"""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class PanelType(str, Enum):
    """预测面板类型"""
    ASTRO = "astro"              # 占星学预测
    CLIMATE = "climate"          # 气候预测
    MACRO_EVENT = "macro_event"  # 宏观事件


@dataclass
class PredictionRecord:
    """预测记录数据类"""
    id: str                           # 预测ID
    panel_type: str                   # 面板类型
    stock_code: str                   # 股票代码
    event_date: str                   # 事件日期 (ISO格式)
    prediction_date: str              # 预测发布日期
    prediction: Dict[str, Any]        # 预测详情 (JSON)
    confidence: float                 # 预测置信度 (0.0-1.0)
    actual_result: Optional[Dict]     # 实际结果 (事后填充)
    accurate: Optional[bool]          # 是否准确 (事后填充)
    validated_at: Optional[str]       # 验证时间
    created_at: str                   # 创建时间
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


class AccuracyTracker:
    """
    准确率追踪系统
    
    工作流程:
    1. 预测发布时调用 record_prediction()
    2. 预测期满后调用 validate_prediction()
    3. 定期调用 get_panel_accuracy() 获取统计
    4. 调用 get_accuracy_trends() 获取趋势数据
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        初始化追踪系统
        
        Args:
            db_path: 数据库路径 (默认: ./data/accuracy_records.db)
        """
        if db_path is None:
            db_path = "./data/accuracy_records.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self) -> None:
        """初始化数据库表"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id TEXT PRIMARY KEY,
                panel_type TEXT NOT NULL,
                stock_code TEXT,
                event_date TEXT NOT NULL,
                prediction_date TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL,
                actual_result TEXT,
                accurate BOOLEAN,
                validated_at TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accuracy_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                panel_type TEXT NOT NULL,
                month TEXT NOT NULL,
                total_predictions INTEGER,
                accurate_predictions INTEGER,
                accuracy REAL,
                sample_size INTEGER,
                created_at TEXT NOT NULL,
                UNIQUE(panel_type, month)
            )
        """)
        
        conn.commit()
        conn.close()
        logger.debug(f"Accuracy database initialized at {self.db_path}")
    
    def record_prediction(
        self,
        panel_type: str,              # 'astro' / 'climate' / 'macro_event'
        stock_code: str,
        event_date: str,              # ISO格式: '2026-06-20'
        prediction: Dict[str, Any],
        confidence: float = 0.5,      # 0.0-1.0
    ) -> str:
        """
        记录一条预测
        
        Args:
            panel_type: 预测面板类型
            stock_code: 股票代码
            event_date: 预测事件日期
            prediction: 预测详情字典
            confidence: 预测置信度
            
        Returns:
            prediction_id (用于后续验证)
            
        Example:
            >>> tracker = AccuracyTracker()
            >>> pred_id = tracker.record_prediction(
            ...     panel_type='astro',
            ...     stock_code='600519',
            ...     event_date='2026-06-21',
            ...     prediction={'expected_direction': 'bullish', 'reason': '夏至吉日'},
            ...     confidence=0.75
            ... )
        """
        try:
            prediction_id = self._generate_prediction_id()
            now = datetime.now().isoformat()
            
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO predictions (
                    id, panel_type, stock_code, event_date, prediction_date,
                    prediction, confidence, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                prediction_id,
                panel_type,
                stock_code,
                event_date,
                now,
                json.dumps(prediction, ensure_ascii=False),
                confidence,
                now,
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(
                f"[Accuracy] Recorded prediction {prediction_id}: "
                f"{panel_type}/{stock_code}/{event_date} (confidence: {confidence:.0%})"
            )
            return prediction_id
            
        except Exception as e:
            logger.error(f"[Accuracy] Failed to record prediction: {e}")
            raise
    
    def validate_prediction(
        self,
        prediction_id: str,
        actual_result: Dict[str, Any],
    ) -> bool:
        """
        事后验证预测准确性
        
        Args:
            prediction_id: 预测ID
            actual_result: 实际结果字典
                          应包含足够的字段用于对比
            
        Returns:
            是否准确
            
        Example:
            >>> tracker.validate_prediction(
            ...     prediction_id='pred_20260620_001',
            ...     actual_result={'actual_direction': 'bullish', 'price_change': '+2.5%'}
            ... )
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # 获取原始预测记录
            cursor.execute(
                "SELECT * FROM predictions WHERE id = ?",
                (prediction_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                logger.warning(f"[Accuracy] Prediction record not found: {prediction_id}")
                return False
            
            # 解析记录
            (
                id_, panel_type, stock_code, event_date, prediction_date,
                prediction_json, confidence, _, _, _, created_at
            ) = row
            
            prediction = json.loads(prediction_json)
            
            # 对比逻辑
            accurate = self._compare_results(panel_type, prediction, actual_result)
            validated_at = datetime.now().isoformat()
            
            # 更新数据库
            cursor.execute("""
                UPDATE predictions
                SET actual_result = ?, accurate = ?, validated_at = ?
                WHERE id = ?
            """, (
                json.dumps(actual_result, ensure_ascii=False),
                accurate,
                validated_at,
                prediction_id,
            ))
            
            conn.commit()
            conn.close()
            
            status = "✓ 准确" if accurate else "✗ 失误"
            logger.info(f"[Accuracy] Validated prediction {prediction_id}: {status}")
            
            return accurate
            
        except Exception as e:
            logger.error(f"[Accuracy] Failed to validate prediction {prediction_id}: {e}")
            raise
    
    def get_panel_accuracy(
        self,
        panel_type: Optional[str] = None,
        days: int = 90,
    ) -> float:
        """
        获取指定时间内的面板准确率
        
        Args:
            panel_type: 面板类型 (None=全部)
            days: 回溯天数
            
        Returns:
            准确率 (0.0-1.0)
            
        Example:
            >>> accuracy = tracker.get_panel_accuracy('astro', days=90)
            >>> print(f"Accuracy: {accuracy:.1%}")  # 输出: Accuracy: 62.5%
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            if panel_type:
                cursor.execute("""
                    SELECT COUNT(*), SUM(CASE WHEN accurate = 1 THEN 1 ELSE 0 END)
                    FROM predictions
                    WHERE panel_type = ? AND validated_at IS NOT NULL
                    AND created_at >= ?
                """, (panel_type, cutoff_date))
            else:
                cursor.execute("""
                    SELECT COUNT(*), SUM(CASE WHEN accurate = 1 THEN 1 ELSE 0 END)
                    FROM predictions
                    WHERE validated_at IS NOT NULL AND created_at >= ?
                """, (cutoff_date,))
            
            result = cursor.fetchone()
            conn.close()
            
            total, accurate_count = result if result else (0, 0)
            
            if total == 0:
                logger.debug(f"[Accuracy] No validated predictions found for {panel_type}")
                return 0.5  # 默认中立值
            
            accuracy = accurate_count / total
            logger.debug(
                f"[Accuracy] {panel_type or 'all'}: {accuracy:.1%} "
                f"({accurate_count}/{total} in last {days}d)"
            )
            
            return accuracy
            
        except Exception as e:
            logger.error(f"[Accuracy] Failed to get panel accuracy: {e}")
            return 0.5
    
    def get_accuracy_trends(
        self,
        panel_type: str,
        window_days: int = 30,
    ) -> List[Dict[str, Any]]:
        """
        获取准确率趋势数据（按周/月聚合）
        
        Args:
            panel_type: 面板类型
            window_days: 聚合窗口 (30=按月, 7=按周)
            
        Returns:
            [
                {
                    'period': '2026-05-01',
                    'accuracy': 0.65,
                    'sample_size': 12,
                    'accurate_count': 8,
                },
                ...
            ]
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # 查询所有已验证的预测
            cursor.execute("""
                SELECT created_at, accurate
                FROM predictions
                WHERE panel_type = ? AND validated_at IS NOT NULL
                ORDER BY created_at ASC
            """, (panel_type,))
            
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                return []
            
            # 按时间窗口聚合
            trends = {}
            for created_at_str, accurate in rows:
                created_at = datetime.fromisoformat(created_at_str)
                
                # 确定窗口期 (按天数算)
                if window_days == 30:
                    period_key = created_at.strftime('%Y-%m-01')  # 按月
                else:
                    # 按周
                    week_start = created_at - timedelta(days=created_at.weekday())
                    period_key = week_start.strftime('%Y-%m-%d')
                
                if period_key not in trends:
                    trends[period_key] = {'accurate': 0, 'total': 0}
                
                trends[period_key]['total'] += 1
                if accurate:
                    trends[period_key]['accurate'] += 1
            
            # 生成结果
            result = []
            for period, stats in sorted(trends.items()):
                accuracy = stats['accurate'] / stats['total'] if stats['total'] > 0 else 0.5
                result.append({
                    'period': period,
                    'accuracy': accuracy,
                    'sample_size': stats['total'],
                    'accurate_count': stats['accurate'],
                })
            
            return result
            
        except Exception as e:
            logger.error(f"[Accuracy] Failed to get accuracy trends: {e}")
            return []
    
    def get_monthly_accuracy_report(self) -> Dict[str, Dict[str, Any]]:
        """
        生成月度准确率报告
        
        Returns:
            {
                'astro': {
                    'predictions': 24,
                    'accurate': 15,
                    'accuracy': 0.625,
                    'trend': '+3%',
                },
                'climate': {...},
                'macro_event': {...},
            }
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # 获取本月的准确率
            now = datetime.now()
            month_start = now.replace(day=1).isoformat()
            
            report = {}
            for panel_type in [PanelType.ASTRO.value, PanelType.CLIMATE.value, PanelType.MACRO_EVENT.value]:
                # 本月数据
                cursor.execute("""
                    SELECT COUNT(*), SUM(CASE WHEN accurate = 1 THEN 1 ELSE 0 END)
                    FROM predictions
                    WHERE panel_type = ? AND validated_at IS NOT NULL
                    AND created_at >= ?
                """, (panel_type, month_start))
                
                result = cursor.fetchone()
                this_month_total, this_month_accurate = result if result else (0, 0)
                
                # 上月数据 (用于趋势比较)
                last_month_start = (now.replace(day=1) - timedelta(days=1)).replace(day=1).isoformat()
                last_month_end = now.replace(day=1).isoformat()
                
                cursor.execute("""
                    SELECT COUNT(*), SUM(CASE WHEN accurate = 1 THEN 1 ELSE 0 END)
                    FROM predictions
                    WHERE panel_type = ? AND validated_at IS NOT NULL
                    AND created_at >= ? AND created_at < ?
                """, (panel_type, last_month_start, last_month_end))
                
                result = cursor.fetchone()
                last_month_total, last_month_accurate = result if result else (0, 0)
                
                # 计算趋势
                this_month_accuracy = this_month_accurate / this_month_total if this_month_total > 0 else 0
                last_month_accuracy = last_month_accurate / last_month_total if last_month_total > 0 else 0
                trend = (this_month_accuracy - last_month_accuracy)
                trend_str = f"+{trend:.1%}" if trend >= 0 else f"{trend:.1%}"
                
                report[panel_type] = {
                    'predictions': this_month_total,
                    'accurate': this_month_accurate,
                    'accuracy': this_month_accuracy,
                    'accuracy_percent': f"{this_month_accuracy:.1%}",
                    'trend': trend_str,
                    'sample_size': this_month_total,
                }
            
            conn.close()
            return report
            
        except Exception as e:
            logger.error(f"[Accuracy] Failed to generate monthly report: {e}")
            return {}
    
    def check_accuracy_threshold(
        self,
        panel_type: str,
        threshold: float = 0.50,
    ) -> bool:
        """
        检查某个面板的准确率是否低于阈值
        
        Args:
            panel_type: 面板类型
            threshold: 准确率阈值 (默认50%)
            
        Returns:
            True if accuracy < threshold
        """
        accuracy = self.get_panel_accuracy(panel_type, days=90)
        
        if accuracy < threshold:
            logger.warning(
                f"[Accuracy] {panel_type} accuracy ({accuracy:.1%}) "
                f"below threshold ({threshold:.1%})"
            )
            return True
        
        return False
    
    def get_prediction_record(self, prediction_id: str) -> Optional[PredictionRecord]:
        """获取单条预测记录详情"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM predictions WHERE id = ?",
                (prediction_id,)
            )
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            (
                id_, panel_type, stock_code, event_date, prediction_date,
                prediction_json, confidence, actual_result_json,
                accurate, validated_at, created_at
            ) = row
            
            return PredictionRecord(
                id=id_,
                panel_type=panel_type,
                stock_code=stock_code,
                event_date=event_date,
                prediction_date=prediction_date,
                prediction=json.loads(prediction_json),
                confidence=confidence,
                actual_result=json.loads(actual_result_json) if actual_result_json else None,
                accurate=accurate,
                validated_at=validated_at,
                created_at=created_at,
            )
            
        except Exception as e:
            logger.error(f"[Accuracy] Failed to get prediction record: {e}")
            return None
    
    # ============ 辅助方法 ============
    
    @staticmethod
    def _generate_prediction_id() -> str:
        """生成预测ID"""
        import uuid
        return f"pred_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}"
    
    @staticmethod
    def _compare_results(
        panel_type: str,
        predicted: Dict[str, Any],
        actual: Dict[str, Any],
    ) -> bool:
        """
        根据预测类型对比预测与实际结果
        
        Args:
            panel_type: 面板类型
            predicted: 预测内容
            actual: 实际结果
            
        Returns:
            是否准确
        """
        try:
            if panel_type == PanelType.ASTRO.value:
                # 对比方向预测 (bullish/neutral/bearish)
                pred_direction = predicted.get('expected_direction', '').lower()
                actual_direction = actual.get('actual_direction', '').lower()
                
                if not pred_direction or not actual_direction:
                    return False
                
                return pred_direction == actual_direction
            
            elif panel_type == PanelType.CLIMATE.value:
                # 对比极端天气是否发生
                pred_severity = predicted.get('severity', '').lower()
                actual_occurred = actual.get('occurred', False)
                
                # 预测无事件但实际无事件 = 准确
                if pred_severity == 'low' and not actual_occurred:
                    return True
                
                # 预测有事件且实际有事件 = 准确
                if actual_occurred:
                    actual_severity = actual.get('actual_severity', '').lower()
                    return pred_severity == actual_severity
                
                return False
            
            elif panel_type == PanelType.MACRO_EVENT.value:
                # 对比宏观事件是否发生
                occurred = actual.get('occurred', False)
                return occurred
            
            return False
            
        except Exception as e:
            logger.error(f"[Accuracy] Error comparing results: {e}")
            return False


# 全局单例
_accuracy_tracker_instance: Optional[AccuracyTracker] = None


def get_accuracy_tracker(db_path: Optional[str] = None) -> AccuracyTracker:
    """获取全局准确率追踪器实例"""
    global _accuracy_tracker_instance
    if _accuracy_tracker_instance is None:
        _accuracy_tracker_instance = AccuracyTracker(db_path)
    return _accuracy_tracker_instance
