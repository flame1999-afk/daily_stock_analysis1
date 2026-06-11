# -*- coding: utf-8 -*-
"""
Industry Five-Element Mapping - 行业五行映射

根据五行属性预测板块轮动
"""

from __future__ import annotations

import logging
from typing import Dict, List, Set

logger = logging.getLogger(__name__)


class IndustryFiveElementMapper:
    """
    行业与五行属性映射器
    
    基本原理：
    - 五行循环：木→火→土→金→水→木
    - 五行相生期为强势期 (约15天)
    - 五行衰落期对相应行业有压力
    """
    
    def __init__(self):
        # 行业与五行的详细映射
        self.industry_elements = {
            # 金行：金属、金融、保险
            'METAL': [
                '有色金属', '贵金属', '金', '银',
                '银行', '保险', '券商', '金融科技',
                '钢铁', '铜', '铝', '镍', '稀土',
                '采矿', '矿业',
            ],
            
            # 木行：农业、医药、教育、纺织
            'WOOD': [
                '农业', '林业', '种植',
                '医药', '生物制药', '中医药', '医疗器械',
                '教育', '培训',
                '纺织', '服装', '家纺',
                '食品', '饮用水',
            ],
            
            # 水行：水利、运输、能源、饮料
            'WATER': [
                '水利', '水电',
                '运输', '物流', '港口', '航运', '高速公路',
                '能源', '石油', '天然气', '电气设备',
                '饮料', '酒类', '葡萄酒',
                '旅游', '酒店',
            ],
            
            # 火行：电力、电子、化工、制造、房地产
            'FIRE': [
                '电力', '电网',
                '电子', '芯片', '半导体', '消费电子',
                '化工', '化肥',
                '汽车', '汽车零部件',
                '房地产', '地产',
                '纸浆纸业',
            ],
            
            # 土行：建筑、建材、陶瓷、矿产
            'EARTH': [
                '建筑', '建筑装饰',
                '建材', '水泥', '陶瓷', '玻璃',
                '矿产', '煤炭',
                '工程机械',
            ],
        }
        
        # 反向映射：行业 -> 五行
        self.industry_to_element = {}
        for element, industries in self.industry_elements.items():
            for industry in industries:
                self.industry_to_element[industry] = element
    
    def get_sector_elements(self) -> Dict[str, List[str]]:
        """
        获取所有行业的五行属性映射
        
        Returns:
            {
                '金': ['有色金属', '银行', ...],
                '木': [...],
                ...
            }
        """
        return self.industry_elements
    
    def get_company_element(self, stock_code: str) -> Dict[str, str]:
        """
        获取特定公司的五行属性
        
        Args:
            stock_code: 股票代码
            
        Returns:
            {
                'code': '600519',
                'name': '贵州茅台',
                'element': 'WATER',
                'reason': '酒类饮料行业属水',
            }
        """
        # TODO: 从数据源获取公司名称和行业
        # 这里使用示例
        
        company_info = {
            '600519': {
                'name': '贵州茅台',
                'industry': '酒类',
            },
            'hk00700': {
                'name': '腾讯控股',
                'industry': '电子',
            },
            'AAPL': {
                'name': 'Apple Inc',
                'industry': '电子',
            },
        }
        
        if stock_code in company_info:
            info = company_info[stock_code]
            element = self.industry_to_element.get(info['industry'], 'EARTH')
            return {
                'code': stock_code,
                'name': info['name'],
                'element': element,
                'element_name': self._element_to_name(element),
                'reason': f"{info['industry']}行业属{self._element_to_name(element)}",
            }
        
        return {
            'code': stock_code,
            'name': '未知',
            'element': 'EARTH',
            'element_name': '土',
            'reason': '行业信息未找到，默认归为土',
        }
    
    def get_current_phase_sectors(
        self,
        current_element: str = 'FIRE',  # 当前主导五行
    ) -> Dict[str, any]:
        """
        预测当前五行主导期的优势板块
        
        Args:
            current_element: 当前主导五行 (如 'FIRE' = 火行)
            
        Returns:
            {
                'current_element': '火',
                'phase_period': '2026-06-05 ~ 2026-06-21 (夏至)',
                'strengthened_sectors': ['电子', '电力', ...],
                'weakened_sectors': ['农业', '水利', ...],
                'recommendation': '该阶段关注火行板块的龙头股',
            }
        """
        if current_element not in self.industry_elements:
            current_element = 'EARTH'
        
        current_element_name = self._element_to_name(current_element)
        
        # 获取当前五行的强势行业
        strengthened = self.industry_elements.get(current_element, [])
        
        # 获取被克制的五行的行业
        conflicting_element = self._get_conflicting_element(current_element)
        weakened = self.industry_elements.get(conflicting_element, [])
        
        return {
            'current_element': current_element_name,
            'current_element_code': current_element,
            'phase_period': '2026-06-05 ~ 2026-06-21 (夏至)',  # 示例
            'strengthened_sectors': strengthened[:10],  # 前10个
            'weakened_sectors': weakened[:5],
            'recommendation': f"该阶段{current_element_name}行板块处于强势期，关注{current_element_name}行龙头股的投资机会",
            'caution': f"{self._element_to_name(conflicting_element)}行板块处于衰落期，需要谨慎",
        }
    
    def get_phase_rotation_forecast(self, days_ahead: int = 30) -> List[Dict[str, any]]:
        """
        获取未来的五行阶段轮动预测
        
        Returns:
            [
                {
                    'start_date': '2026-06-05',
                    'end_date': '2026-06-20',
                    'element': '火',
                    'solar_term': '芒种→夏至',
                    'duration_days': 16,
                    'sector_focus': ['电子', '电力', ...],
                },
                {
                    'start_date': '2026-06-21',
                    'end_date': '2026-07-07',
                    'element': '土',
                    'solar_term': '夏至→小暑',
                    'duration_days': 17,
                    'sector_focus': ['建筑', '建材', ...],
                },
                ...
            ]
        """
        # TODO: 实现完整的五行轮动预测
        # 需要结合节气信息
        
        forecast = []
        # 示例数据
        current_phase = {
            'start_date': '2026-06-05',
            'end_date': '2026-06-20',
            'element': '火',
            'element_name': self._element_to_name('FIRE'),
            'solar_term': '芒种→夏至',
            'duration_days': 16,
            'sector_focus': self.industry_elements.get('FIRE', [])[:5],
        }
        forecast.append(current_phase)
        
        return forecast
    
    def analyze_sector_performance(
        self,
        sector: str,
        current_element: str,
    ) -> Dict[str, any]:
        """
        分析特定行业在当前五行阶段的表现预期
        
        Args:
            sector: 行业名称
            current_element: 当前主导五行
            
        Returns:
            {
                'sector': '医药',
                'sector_element': '木',
                'current_element': '火',
                'relationship': '木生火',  # or 相克、相同
                'expected_performance': 'bullish',  # bullish/neutral/bearish
                'rationale': '火行旺盛期，木行衰落，医药行业处于相对弱势',
            }
        """
        sector_element = self.industry_to_element.get(sector, 'EARTH')
        
        # 分析五行关系
        relationship = self._analyze_element_relationship(sector_element, current_element)
        
        # 判断预期表现
        if relationship == '相生':
            expected_performance = 'bullish'
            rationale = f"{self._element_to_name(sector_element)}行生{self._element_to_name(current_element)}行，该行业处于强势期"
        elif relationship == '相克':
            expected_performance = 'bearish'
            rationale = f"{self._element_to_name(current_element)}行克{self._element_to_name(sector_element)}行，该行业承压"
        else:
            expected_performance = 'neutral'
            rationale = "五行无直接关系，表现中性"
        
        return {
            'sector': sector,
            'sector_element': self._element_to_name(sector_element),
            'current_element': self._element_to_name(current_element),
            'relationship': relationship,
            'expected_performance': expected_performance,
            'rationale': rationale,
        }
    
    # ============ 辅助方法 ============
    
    @staticmethod
    def _element_to_name(element: str) -> str:
        """将五行代码转换为中文名称"""
        names = {
            'METAL': '金',
            'WOOD': '木',
            'WATER': '水',
            'FIRE': '火',
            'EARTH': '土',
        }
        return names.get(element, '土')
    
    @staticmethod
    def _get_conflicting_element(element: str) -> str:
        """获取相克的五行"""
        conflicts = {
            'METAL': 'WOOD',   # 金克木
            'WOOD': 'EARTH',   # 木克土
            'EARTH': 'WATER',  # 土克水
            'WATER': 'FIRE',   # 水克火
            'FIRE': 'METAL',   # 火克金
        }
        return conflicts.get(element, 'EARTH')
    
    @staticmethod
    def _analyze_element_relationship(elem1: str, elem2: str) -> str:
        """分析两个五行的关系"""
        generation = {
            'METAL': 'WATER',
            'WATER': 'WOOD',
            'WOOD': 'FIRE',
            'FIRE': 'EARTH',
            'EARTH': 'METAL',
        }
        
        if generation.get(elem1) == elem2:
            return '相生'
        
        conflict = {
            'METAL': 'WOOD',
            'WOOD': 'EARTH',
            'EARTH': 'WATER',
            'WATER': 'FIRE',
            'FIRE': 'METAL',
        }
        
        if conflict.get(elem1) == elem2 or conflict.get(elem2) == elem1:
            return '相克'
        
        if elem1 == elem2:
            return '相同'
        
        return '无关'
