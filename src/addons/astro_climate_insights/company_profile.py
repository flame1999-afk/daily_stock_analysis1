# -*- coding: utf-8 -*-
"""
Company Astro Profile - 企业运势分析

基于企业成立日期和行业属性的五行运势分析
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class CompanyAstroProfile:
    """
    企业占星学档案
    
    分析维度：
    1. 企业成立日期的五行属性
    2. 行业属性的五行
    3. 五行生克关系
    4. 当前节气与企业的兼容度
    5. 长期大运周期
    """
    
    def __init__(self):
        # 行业与五行的映射
        self.industry_element_mapping = {
            # 金行：金属、金融、保险
            '有色金属': 'METAL',
            '贵金属': 'METAL',
            '银行': 'METAL',
            '保险': 'METAL',
            '钢铁': 'METAL',
            '采矿': 'METAL',
            
            # 木行：农业、医药、教育
            '农业': 'WOOD',
            '林业': 'WOOD',
            '教育': 'WOOD',
            '医药': 'WOOD',
            '生物': 'WOOD',
            '纺织': 'WOOD',
            
            # 水行：水利、运输、能源
            '水利': 'WATER',
            '运输': 'WATER',
            '物流': 'WATER',
            '能源': 'WATER',
            '石油': 'WATER',
            '饮料': 'WATER',
            '酒类': 'WATER',
            '旅游': 'WATER',
            
            # 火行：电力、电子、化工
            '电力': 'FIRE',
            '电子': 'FIRE',
            '化工': 'FIRE',
            '制造': 'FIRE',
            '房地产': 'FIRE',
            '汽车': 'FIRE',
            
            # 土行：房地产、建筑、陶瓷
            '建筑': 'EARTH',
            '陶瓷': 'EARTH',
            '水泥': 'EARTH',
            '矿产': 'EARTH',
        }
        
        # 五行生克关系
        self.element_generation = {
            'METAL': 'WATER',   # 金生水
            'WATER': 'WOOD',    # 水生木
            'WOOD': 'FIRE',     # 木生火
            'FIRE': 'EARTH',    # 火生土
            'EARTH': 'METAL',   # 土生金
        }
        
        self.element_conflict = {
            'METAL': 'WOOD',    # 金克木
            'WOOD': 'EARTH',    # 木克土
            'EARTH': 'WATER',   # 土克水
            'WATER': 'FIRE',    # 水克火
            'FIRE': 'METAL',    # 火克金
        }
    
    def analyze_company_destiny(
        self,
        stock_code: str,
        company_name: Optional[str] = None,
        established_date: Optional[str] = None,
        industry: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        分析企业运势
        
        Args:
            stock_code: 股票代码
            company_name: 公司名称
            established_date: 成立日期 (ISO格式)
            industry: 所属行业
            
        Returns:
            {
                'stock_code': '600519',
                'company_name': '贵州茅台',
                'established_date': '1951-12-21',
                'establishment_element': '金',
                'company_element': '水',
                'element_harmony': '金生水',
                'harmony_score': 8,
                'current_phase_compatibility': 7,
                'micro_cycle_outlook': '看好',
                'macro_cycle_outlook': '持续向好',
                'risk_points': [...],
            }
        """
        try:
            # TODO: 从数据源获取企业信息
            # 这里使用示例数据
            
            # 获取成立日期的五行
            if established_date:
                established_dt = datetime.fromisoformat(established_date)
                from .calendar_engine import get_calendar_engine
                engine = get_calendar_engine()
                element_info = engine.get_element_by_date(established_dt)
                establishment_element = element_info.get('element', '土')
            else:
                establishment_element = '土'  # 默认
            
            # 获取公司行业五行
            company_element = self._get_industry_element(industry or '')
            
            # 计算五行兼容度
            harmony = self._calculate_harmony(establishment_element, company_element)
            harmony_score, harmony_desc = harmony
            
            # 获取当前阶段兼容度
            from .calendar_engine import get_calendar_engine
            engine = get_calendar_engine()
            current_element_info = engine.get_element_by_date(datetime.now())
            current_element = current_element_info.get('element', '土')
            
            phase_compatibility = self._calculate_phase_compatibility(
                establishment_element,
                company_element,
                current_element
            )
            
            # 获取大运周期
            macro_cycle = self._get_macro_cycle(established_date)
            
            # 识别风险点
            risk_points = self._identify_risk_points(
                establishment_element,
                company_element,
                current_element
            )
            
            return {
                'stock_code': stock_code,
                'company_name': company_name or '未知',
                'established_date': established_date or '未知',
                'establishment_element': establishment_element,
                'company_element': company_element,
                'element_harmony': harmony_desc,
                'harmony_score': harmony_score,
                'current_phase_compatibility': phase_compatibility,
                'micro_cycle_outlook': self._get_micro_outlook(
                    harmony_score,
                    phase_compatibility
                ),
                'macro_cycle_outlook': macro_cycle.get('outlook', '中性'),
                'macro_cycle_period': macro_cycle.get('period', '未知'),
                'risk_points': risk_points,
            }
        except Exception as e:
            logger.error(f"Failed to analyze company destiny for {stock_code}: {e}")
            return {}
    
    def get_macro_cycle_status(self, stock_code: str) -> Dict[str, Any]:
        """
        获取企业的长期大运周期状态
        
        Returns:
            {
                'current_cycle': '长期上升周期 (2020-2030)',
                'cycle_start': '2020-01-01',
                'cycle_end': '2030-12-31',
                'cycle_strength': 'strong',
                'expected_returns': '年化5-15%',
                'cycle_phase': 'rising',  # rising / peak / declining / bottom
            }
        """
        # TODO: 实现基于企业历史数据的大运周期分析
        return {
            'current_cycle': '分析中',
            'cycle_start': None,
            'cycle_end': None,
            'cycle_strength': 'unknown',
            'expected_returns': '未知',
        }
    
    # ============ 辅助方法 ============
    
    def _get_industry_element(self, industry: str) -> str:
        """根据行业获取五行属性"""
        for ind, element in self.industry_element_mapping.items():
            if ind in industry:
                return element
        return 'EARTH'  # 默认土
    
    def _calculate_harmony(self, elem1: str, elem2: str) -> tuple:
        """
        计算两个五行的兼容度
        
        Returns:
            (兼容度分数 0-10, 描述)
        """
        # 相生 (最佳)
        if self.element_generation.get(elem1) == elem2:
            return (9, f"{elem1}生{elem2}")
        if self.element_generation.get(elem2) == elem1:
            return (8, f"{elem2}生{elem1}")
        
        # 相克 (最差)
        if self.element_conflict.get(elem1) == elem2:
            return (2, f"{elem1}克{elem2}")
        if self.element_conflict.get(elem2) == elem1:
            return (3, f"{elem2}克{elem1}")
        
        # 相同 (中性)
        if elem1 == elem2:
            return (5, f"{elem1}同性")
        
        # 其他 (中性)
        return (5, "五行平衡")
    
    def _calculate_phase_compatibility(self, elem_established: str, elem_company: str, elem_current: str) -> int:
        """
        计算当前节气与企业的兼容度
        
        基于：当前五行 vs 企业五行
        """
        score, _ = self._calculate_harmony(elem_current, elem_company)
        return min(10, max(1, score))
    
    def _get_micro_outlook(self, harmony_score: int, phase_compatibility: int) -> str:
        """获取短期展望"""
        avg_score = (harmony_score + phase_compatibility) / 2
        
        if avg_score >= 8:
            return '看好'
        elif avg_score >= 6:
            return '中性偏好'
        elif avg_score >= 4:
            return '中性'
        else:
            return '看空'
    
    def _get_macro_cycle(self, established_date: Optional[str]) -> Dict[str, Any]:
        """获取企业的大运周期"""
        if not established_date:
            return {'outlook': '未知', 'period': '无法确定'}
        
        try:
            est_dt = datetime.fromisoformat(established_date)
            now = datetime.now()
            age_years = (now - est_dt).days / 365.25
            
            # 简化版：根据企业年龄判断
            if age_years < 5:
                return {'outlook': '快速成长期', 'period': '未来可期'}
            elif age_years < 15:
                return {'outlook': '稳定发展期', 'period': '预期正常增长'}
            elif age_years < 30:
                return {'outlook': '成熟稳定期', 'period': '预期保持现状或衰退'}
            else:
                return {'outlook': '衰退或重生期', 'period': '需要观察转折'}
        except:
            return {'outlook': '未知', 'period': '分析出错'}
    
    def _identify_risk_points(self, elem_est: str, elem_company: str, elem_current: str) -> list:
        """识别风险点"""
        risks = []
        
        # 五行冲突风险
        if self.element_conflict.get(elem_current) == elem_company:
            risks.append(f"当前{elem_current}行衰落阶段，{elem_company}行企业可能面临压力")
        
        # 企业本身五行冲突
        if self.element_conflict.get(elem_est) == elem_company:
            risks.append("企业成立日期五行与行业五行相克，需加强风控")
        
        return risks
