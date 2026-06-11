# -*- coding: utf-8 -*-
"""
Integration Module - 与主分析流程的集成

负责将补充洞察集成到核心分析管道
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class AstroClimateInsightIntegrator:
    """
    占星学与气候洞察集成器
    
    功能：
    1. 调用补充洞察引擎
    2. 格式化输出
    3. 与主流程集成
    """
    
    def __init__(self):
        from .insight_synthesizer import SupplementaryInsightSynthesizer
        self.synthesizer = SupplementaryInsightSynthesizer()
    
    def generate_supplementary_insights(
        self,
        stock_code: str,
        company_name: Optional[str] = None,
        industry: Optional[str] = None,
        established_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        为单只股票生成完整补充洞察
        
        这是主要集成点，被核心分析流程调用
        
        Args:
            stock_code: 股票代码
            company_name: 公司名称
            industry: 行业分类
            established_date: 成立日期
            
        Returns:
            补充洞察字典，包含所有面板和准确率信息
        """
        try:
            insights = self.synthesizer.generate_insights(
                stock_code=stock_code,
                company_name=company_name,
                industry=industry,
                established_date=established_date,
            )
            
            logger.info(f"Generated supplementary insights for {stock_code}")
            return insights
        except Exception as e:
            logger.error(f"Failed to generate supplementary insights for {stock_code}: {e}")
            return self._get_default_insights()
    
    def record_prediction(
        self,
        panel_type: str,
        stock_code: str,
        event_date: str,
        prediction: Dict[str, Any],
        confidence: float = 0.5,
    ) -> Optional[str]:
        """
        记录一条预测（供事后验证）
        
        Args:
            panel_type: 'astro' / 'climate' / 'macro_event'
            stock_code: 股票代码
            event_date: 事件日期
            prediction: 预测详情
            confidence: 置信度
            
        Returns:
            prediction_id
        """
        try:
            from .accuracy_tracker import get_accuracy_tracker
            tracker = get_accuracy_tracker()
            
            pred_id = tracker.record_prediction(
                panel_type=panel_type,
                stock_code=stock_code,
                event_date=event_date,
                prediction=prediction,
                confidence=confidence,
            )
            
            return pred_id
        except Exception as e:
            logger.error(f"Failed to record prediction: {e}")
            return None
    
    def validate_prediction(
        self,
        prediction_id: str,
        actual_result: Dict[str, Any],
    ) -> bool:
        """
        验证已过期的预测
        
        Args:
            prediction_id: 预测ID
            actual_result: 实际结果
            
        Returns:
            是否准确
        """
        try:
            from .accuracy_tracker import get_accuracy_tracker
            tracker = get_accuracy_tracker()
            
            accurate = tracker.validate_prediction(
                prediction_id=prediction_id,
                actual_result=actual_result,
            )
            
            return accurate
        except Exception as e:
            logger.error(f"Failed to validate prediction: {e}")
            return False
    
    def get_accuracy_report(self, days: int = 90) -> Dict[str, Any]:
        """
        获取准确率报告
        
        Returns:
            {
                'astro': {'accuracy': 0.62, 'sample_size': 231, ...},
                'climate': {...},
                'macro_event': {...},
            }
        """
        try:
            from .accuracy_tracker import get_accuracy_tracker
            tracker = get_accuracy_tracker()
            
            report = tracker.get_monthly_accuracy_report()
            return report
        except Exception as e:
            logger.error(f"Failed to get accuracy report: {e}")
            return {}
    
    def check_accuracy_alerts(self) -> Dict[str, bool]:
        """
        检查准确率是否低于阈值
        
        Returns:
            {
                'astro_low_accuracy': False,
                'climate_low_accuracy': False,
                'macro_event_low_accuracy': True,
            }
        """
        try:
            from .accuracy_tracker import get_accuracy_tracker
            tracker = get_accuracy_tracker()
            
            alerts = {
                'astro_low_accuracy': tracker.check_accuracy_threshold('astro', threshold=0.50),
                'climate_low_accuracy': tracker.check_accuracy_threshold('climate', threshold=0.65),
                'macro_event_low_accuracy': tracker.check_accuracy_threshold('macro_event', threshold=0.50),
            }
            
            return alerts
        except Exception as e:
            logger.error(f"Failed to check accuracy alerts: {e}")
            return {}
    
    @staticmethod
    def _get_default_insights() -> Dict[str, Any]:
        """
        返回默认的补充洞察（当生成失败时）
        """
        return {
            'analysis_date': datetime.now().date().isoformat(),
            'astro_panel': None,
            'astro_accuracy': 0.5,
            'astro_accuracy_percent': '50%',
            'astro_sample_size': 0,
            'climate_panel': None,
            'climate_accuracy': 0.5,
            'climate_accuracy_percent': '50%',
            'climate_sample_size': 0,
            'macro_events_panel': None,
            'macro_accuracy': 0.5,
            'macro_accuracy_percent': '50%',
            'macro_sample_size': 0,
            'key_insights': [],
            'opportunities': [],
            'risk_flags': [],
        }


# 全局集成器实例
_integrator_instance: Optional[AstroClimateInsightIntegrator] = None


def get_integrator() -> AstroClimateInsightIntegrator:
    """
    获取全局集成器实例
    
    Usage:
        from src.addons.astro_climate_insights.integration import get_integrator
        
        integrator = get_integrator()
        insights = integrator.generate_supplementary_insights(
            stock_code='600519',
            company_name='贵州茅台',
        )
    """
    global _integrator_instance
    if _integrator_instance is None:
        _integrator_instance = AstroClimateInsightIntegrator()
    return _integrator_instance
