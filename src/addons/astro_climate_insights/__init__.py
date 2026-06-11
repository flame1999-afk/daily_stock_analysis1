# -*- coding: utf-8 -*-
"""
Astro Climate Insights Addon - 占星学与气候预测洞察

该模块提供独立的补充分析视角，不影响核心评分。

功能：
1. 占星学洞察 (准确率追踪)
2. 气候与天气预测 (官方数据源)
3. 宏观事件预测 (舆情分析)
4. 准确率追踪与学习

Usage:
    from src.addons.astro_climate_insights import (
        ChineseCalendarEngine,
        AccuracyTracker,
        CompanyAstroProfile,
        AstroInsightEngine,
    )
"""

from __future__ import annotations

from .calendar_engine import (
    ChineseCalendarEngine,
    get_calendar_engine,
    Element,
    YinYang,
    SolarTerm,
    ZodiacAnimal,
)

from .accuracy_tracker import (
    AccuracyTracker,
    get_accuracy_tracker,
    PredictionRecord,
    PanelType,
)

from .company_profile import CompanyAstroProfile
from .event_predictor import MacroEventPredictor
from .industry_mapping import IndustryFiveElementMapper

__all__ = [
    # Calendar Engine
    'ChineseCalendarEngine',
    'get_calendar_engine',
    'Element',
    'YinYang',
    'SolarTerm',
    'ZodiacAnimal',
    
    # Accuracy Tracker
    'AccuracyTracker',
    'get_accuracy_tracker',
    'PredictionRecord',
    'PanelType',
    
    # Company Profile
    'CompanyAstroProfile',
    
    # Event Predictor
    'MacroEventPredictor',
    
    # Industry Mapping
    'IndustryFiveElementMapper',
]

__version__ = '0.1.0'
