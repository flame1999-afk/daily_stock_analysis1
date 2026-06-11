# -*- coding: utf-8 -*-
"""
Insight Synthesizer - 洞察合成与汇总

将所有占星学、气候、宏观事件的分析汇总生成补充洞察面板
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)


class SupplementaryInsightSynthesizer:
    """
    补充洞察合成器
    
    功能：
    1. 调用各个分析模块生成洞察
    2. 合成为统一的补充洞察面板
    3. 关键提示汇总
    4. 风险评估
    """
    
    def __init__(self):
        from .calendar_engine import get_calendar_engine
        from .accuracy_tracker import get_accuracy_tracker
        from .company_profile import CompanyAstroProfile
        from .event_predictor import MacroEventPredictor
        from .industry_mapping import IndustryFiveElementMapper
        
        self.calendar_engine = get_calendar_engine()
        self.accuracy_tracker = get_accuracy_tracker()
        self.company_profile = CompanyAstroProfile()
        self.event_predictor = MacroEventPredictor()
        self.industry_mapper = IndustryFiveElementMapper()
    
    def generate_insights(
        self,
        stock_code: str,
        company_name: Optional[str] = None,
        industry: Optional[str] = None,
        established_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        为单只股票生成完整的补充洞察面板
        
        Args:
            stock_code: 股票代码
            company_name: 公司名称
            industry: 行业分类
            established_date: 成立日期
            
        Returns:
            {
                'astro_panel': {...},
                'astro_accuracy': 0.62,
                'astro_sample_size': 231,
                
                'climate_panel': {...},
                'climate_accuracy': 0.75,
                'climate_sample_size': 145,
                
                'macro_events_panel': {...},
                'macro_accuracy': 0.58,
                'macro_sample_size': 87,
                
                'key_insights': [...],
                'opportunities': [...],
                'risk_flags': [...],
            }
        """
        try:
            analysis_date = datetime.now().date()
            
            # 1. 占星学洞察
            astro_panel = self._generate_astro_panel(
                stock_code,
                company_name,
                industry,
                established_date,
                analysis_date,
            )
            
            # 2. 气候与天气洞察
            climate_panel = self._generate_climate_panel(industry)
            
            # 3. 宏观事件洞察
            macro_panel = self._generate_macro_events_panel()
            
            # 4. 获取准确率
            astro_accuracy = self.accuracy_tracker.get_panel_accuracy('astro')
            climate_accuracy = self.accuracy_tracker.get_panel_accuracy('climate')
            macro_accuracy = self.accuracy_tracker.get_panel_accuracy('macro_event')
            
            # 5. 综合提示
            key_insights = self._synthesize_key_insights(
                astro_panel,
                climate_panel,
                macro_panel,
            )
            
            opportunities = self._identify_opportunities(
                astro_panel,
                climate_panel,
                macro_panel,
            )
            
            risk_flags = self._identify_risks(
                astro_panel,
                climate_panel,
                macro_panel,
            )
            
            return {
                'analysis_date': analysis_date.isoformat(),
                'stock_code': stock_code,
                
                # 占星学面板
                'astro_panel': astro_panel,
                'astro_accuracy': astro_accuracy,
                'astro_accuracy_percent': f"{astro_accuracy:.1%}",
                'astro_sample_size': self._get_sample_size('astro'),
                
                # 气候面板
                'climate_panel': climate_panel,
                'climate_accuracy': climate_accuracy,
                'climate_accuracy_percent': f"{climate_accuracy:.1%}",
                'climate_sample_size': self._get_sample_size('climate'),
                
                # 宏观事件面板
                'macro_events_panel': macro_panel,
                'macro_accuracy': macro_accuracy,
                'macro_accuracy_percent': f"{macro_accuracy:.1%}",
                'macro_sample_size': self._get_sample_size('macro_event'),
                
                # 综合提示
                'key_insights': key_insights,
                'opportunities': opportunities,
                'risk_flags': risk_flags,
            }
        except Exception as e:
            logger.error(f"Failed to generate insights for {stock_code}: {e}")
            return {}
    
    def _generate_astro_panel(
        self,
        stock_code: str,
        company_name: Optional[str],
        industry: Optional[str],
        established_date: Optional[str],
        analysis_date,
    ) -> Dict[str, Any]:
        """
        生成占星学洞察面板
        """
        try:
            # 获取农历信息
            lunar_info = self.calendar_engine.get_lunar_date(analysis_date.isoformat())
            
            # 获取今日吉凶
            fortune_calendar = self.calendar_engine.get_fortune_calendar(
                analysis_date.strftime('%Y-%m')
            )
            today_fortune = next(
                (day for day in fortune_calendar if day['date'] == analysis_date.isoformat()),
                None
            )
            
            # 获取企业运势
            company_destiny = self.company_profile.analyze_company_destiny(
                stock_code,
                company_name,
                established_date,
                industry,
            )
            
            # 获取本月节气
            solar_terms = self.calendar_engine.get_solar_terms_this_month()
            
            return {
                'lunar_date': lunar_info.get('lunar_date', ''),
                'zodiac_animal': lunar_info.get('zodiac_animal', ''),
                'today_fortune': {
                    'level': today_fortune.get('fortune_level', 5) if today_fortune else 5,
                    'heavenly_stem': today_fortune.get('heavenly_stem', '') if today_fortune else '',
                    'earthly_branch': today_fortune.get('earthly_branch', '') if today_fortune else '',
                    'recommendation': today_fortune.get('recommendation', '') if today_fortune else '',
                },
                'sector_phase': self._get_current_sector_phase(),
                'company_destiny': company_destiny,
                'upcoming_solar_terms': solar_terms[:3],
                'predicted_events': self._get_predicted_astro_events(),
            }
        except Exception as e:
            logger.warning(f"Failed to generate astro panel: {e}")
            return {}
    
    def _generate_climate_panel(self, industry: Optional[str]) -> Dict[str, Any]:
        """
        生成气候与天气洞察面板
        """
        try:
            return {
                'seasonal_status': {
                    'season': '初夏',
                    'temperature_trend': 'rising',
                    'description': '气温持续上升，电力需求增加',
                },
                'extreme_weather_alerts': self._get_weather_alerts(),
                'agriculture_outlook': self._get_agriculture_outlook(),
                'logistics_impact': self._get_logistics_impact(),
                'energy_demand': self._get_energy_demand(),
                'commodity_impacts': self._get_commodity_impacts(),
            }
        except Exception as e:
            logger.warning(f"Failed to generate climate panel: {e}")
            return {}
    
    def _generate_macro_events_panel(self) -> Dict[str, Any]:
        """
        生成宏观事件洞察面板
        """
        try:
            # 获取政策事件预测
            policy_events = self.event_predictor.predict_policy_events(forecast_days=30)
            
            return {
                'upcoming_events': policy_events[:5],
                'regulation_outlook': self._get_regulation_outlook(),
                'disaster_risks': self._get_disaster_risks(),
                'macro_sentiment': self._calculate_macro_sentiment(policy_events),
            }
        except Exception as e:
            logger.warning(f"Failed to generate macro events panel: {e}")
            return {}
    
    # ============ 辅助方法 ============
    
    def _get_current_sector_phase(self) -> Dict[str, Any]:
        """
        获取当前五行阶段信息
        """
        try:
            # 基于当前日期的五行属性
            element_info = self.calendar_engine.get_element_by_date(datetime.now())
            current_element = element_info.get('element', '土')
            
            # 获取行业五行映射
            phase_info = self.industry_mapper.get_current_phase_sectors(
                self._element_to_code(current_element)
            )
            
            return {
                'current_element': current_element,
                'phase_info': phase_info,
            }
        except Exception as e:
            logger.debug(f"Failed to get current sector phase: {e}")
            return {}
    
    def _get_predicted_astro_events(self) -> List[Dict[str, Any]]:
        """
        获取占星学预测事件
        """
        try:
            calendar = self.calendar_engine.get_fortune_calendar(
                datetime.now().strftime('%Y-%m')
            )
            
            # 提取关键吉凶日
            key_events = []
            for day in calendar:
                if day['fortune_level'] >= 8 or day['fortune_level'] <= 2:
                    key_events.append({
                        'date': day['date'],
                        'fortune_level': day['fortune_level'],
                        'recommendation': day['recommendation'],
                    })
            
            return key_events[:5]
        except Exception as e:
            logger.debug(f"Failed to get predicted astro events: {e}")
            return []
    
    def _get_weather_alerts(self) -> List[Dict[str, Any]]:
        """
        获取极端天气预警
        """
        # TODO: 集成气候API
        return [
            {
                'date': '2026-06-15',
                'region': '华东地区',
                'event': '高温预警',
                'severity': 'high',
            }
        ]
    
    def _get_agriculture_outlook(self) -> Dict[str, Any]:
        """
        获取农业前景
        """
        # TODO: 集成农业气象数据
        return {
            'crop_status': 'good',
            'yield_expectation': '+3%',
            'price_trend': 'stable',
        }
    
    def _get_logistics_impact(self) -> Dict[str, Any]:
        """
        获取物流影响
        """
        return {
            'transport_delay_risk': 'medium',
            'affected_routes': [],
            'estimated_delay': '1-2小时',
        }
    
    def _get_energy_demand(self) -> Dict[str, Any]:
        """
        获取能源需求展望
        """
        return {
            'heating_cooling_demand': 'high',
            'renewable_generation': 'strong',
            'grid_risk': 'low',
        }
    
    def _get_commodity_impacts(self) -> Dict[str, Any]:
        """
        获取商品影响
        """
        return {
            'oil': 'neutral',
            'grain': 'negative',  # 极端高温
            'power': 'positive',  # 电力需求上升
        }
    
    def _get_regulation_outlook(self) -> Dict[str, Any]:
        """
        获取监管前景
        """
        return {
            'policy_trend': 'neutral',
            'potential_changes': [],
        }
    
    def _get_disaster_risks(self) -> List[Dict[str, Any]]:
        """
        获取自然灾害风险
        """
        return []
    
    def _calculate_macro_sentiment(self, events: List[Dict]) -> str:
        """
        基于事件计算宏观情绪
        """
        bullish_count = sum(1 for e in events if e.get('expected_impact') == 'bullish')
        bearish_count = sum(1 for e in events if e.get('expected_impact') == 'bearish')
        
        if bullish_count > bearish_count * 1.5:
            return 'very_bullish'
        elif bullish_count > bearish_count:
            return 'bullish'
        elif bearish_count > bullish_count * 1.5:
            return 'very_bearish'
        elif bearish_count > bullish_count:
            return 'bearish'
        else:
            return 'neutral'
    
    def _synthesize_key_insights(
        self,
        astro_panel: Dict,
        climate_panel: Dict,
        macro_panel: Dict,
    ) -> List[str]:
        """
        合成关键洞察
        """
        insights = []
        
        # 占星学洞察
        if astro_panel and astro_panel.get('today_fortune', {}).get('level', 5) >= 8:
            insights.append('吉日来临，适合交易操作')
        
        # 气候洞察
        if climate_panel and climate_panel.get('extreme_weather_alerts'):
            insights.append('需关注极端天气对产业链的影响')
        
        return insights[:5]
    
    def _identify_opportunities(
        self,
        astro_panel: Dict,
        climate_panel: Dict,
        macro_panel: Dict,
    ) -> List[str]:
        """
        识别投资机会
        """
        opportunities = []
        
        if astro_panel and astro_panel.get('today_fortune', {}).get('level', 5) >= 8:
            opportunities.append('占星学预示吉日，可适度加仓')
        
        return opportunities[:3]
    
    def _identify_risks(
        self,
        astro_panel: Dict,
        climate_panel: Dict,
        macro_panel: Dict,
    ) -> List[str]:
        """
        识别风险点
        """
        risks = []
        
        if astro_panel and astro_panel.get('today_fortune', {}).get('level', 5) <= 3:
            risks.append('凶日来临，建议谨慎交易')
        
        if climate_panel and climate_panel.get('extreme_weather_alerts'):
            risks.append('极端天气预警，可能影响供应链')
        
        return risks[:3]
    
    def _get_sample_size(self, panel_type: str) -> int:
        """
        获取面板的验证样本数
        """
        try:
            record = self.accuracy_tracker._query_records({
                'panel_type': panel_type,
                'validated': True,
            })
            return len(record)
        except:
            return 0
    
    @staticmethod
    def _element_to_code(element: str) -> str:
        """
        将五行名称转换为代码
        """
        mapping = {
            '金': 'METAL',
            '木': 'WOOD',
            '水': 'WATER',
            '火': 'FIRE',
            '土': 'EARTH',
        }
        return mapping.get(element, 'EARTH')
