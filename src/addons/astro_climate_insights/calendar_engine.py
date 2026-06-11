# -*- coding: utf-8 -*-
"""
Chinese Calendar Engine - 农历/节气/五行计算引擎

该模块提供：
1. 农历日期转换
2. 二十四节气计算
3. 天干地支推算
4. 五行纳音属性
5. 吉凶日期预测
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from enum import Enum

logger = logging.getLogger(__name__)

try:
    from lunarcalendar import Converter, Solar, Lunar
except ImportError:
    logger.warning("lunarcalendar library not installed. Install with: pip install lunarcalendar")
    Converter = None


class Element(str, Enum):
    """五行属性"""
    WOOD = "木"
    FIRE = "火"
    EARTH = "土"
    METAL = "金"
    WATER = "水"


class YinYang(str, Enum):
    """阴阳属性"""
    YIN = "阴"
    YANG = "阳"


class SolarTerm(str, Enum):
    """二十四节气"""
    XIAOHAN = "小寒"          # 1月5-7日
    DAHAN = "大寒"            # 1月20-21日
    LICHUN = "立春"           # 2月3-5日
    JINGZHE = "惊蛰"          # 3月5-7日
    CHUNFEN = "春分"          # 3月20-22日
    QINGMING = "清明"         # 4月4-6日
    GUYU = "谷雨"             # 4月19-21日
    LIXIA = "立夏"            # 5月5-7日
    XIAOMAN = "小满"          # 5月20-22日
    MANGZHONG = "芒种"        # 6月5-7日
    XIAZHI = "夏至"           # 6月20-22日
    XIAOSHU = "小暑"          # 7月6-8日
    DASHU = "大暑"            # 7月22-24日
    LIQIU = "立秋"            # 8月7-9日
    CHUSHU = "处暑"           # 8月22-24日
    QIUFEN = "秋分"           # 9月22-24日
    SHUANGJIANG = "霜降"      # 10月23-24日
    LIDONG = "立冬"           # 11月7-8日
    XIAOXUE = "小雪"          # 11月22-23日
    DAXUE = "大雪"            # 12月6-8日


class ZodiacAnimal(str, Enum):
    """十二生肖"""
    RAT = "鼠"
    OX = "牛"
    TIGER = "虎"
    RABBIT = "兔"
    DRAGON = "龙"
    SNAKE = "蛇"
    HORSE = "马"
    GOAT = "羊"
    MONKEY = "猴"
    ROOSTER = "鸡"
    DOG = "狗"
    PIG = "猪"


# 天干 (10个)
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支 (12个)
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 六十甲子 (干支纪年)
SEXAGENARY_CYCLE = [f"{HEAVENLY_STEMS[i % 10]}{EARTHLY_BRANCHES[i % 12]}" for i in range(60)]

# 五行属性映射 (天干)
HEAVENLY_STEM_ELEMENTS = {
    "甲": Element.WOOD, "乙": Element.WOOD,
    "丙": Element.FIRE, "丁": Element.FIRE,
    "戊": Element.EARTH, "己": Element.EARTH,
    "庚": Element.METAL, "辛": Element.METAL,
    "壬": Element.WATER, "癸": Element.WATER,
}

# 五行属性映射 (地支)
EARTHLY_BRANCH_ELEMENTS = {
    "子": Element.WATER, "丑": Element.EARTH,
    "寅": Element.WOOD, "卯": Element.WOOD,
    "辰": Element.EARTH, "巳": Element.FIRE,
    "午": Element.FIRE, "未": Element.EARTH,
    "申": Element.METAL, "酉": Element.METAL,
    "戌": Element.EARTH, "亥": Element.WATER,
}

# 纳音五行 (六十甲子对应的纳音五行)
NAYIN_ELEMENTS = {
    "甲子": Element.WATER, "乙丑": Element.WATER,
    "丙寅": Element.FIRE, "丁卯": Element.FIRE,
    "戊辰": Element.EARTH, "己巳": Element.EARTH,
    "庚午": Element.GOLD, "辛未": Element.GOLD,
    "壬申": Element.WATER, "癸酉": Element.WATER,
    "甲戌": Element.FIRE, "乙亥": Element.FIRE,
    "丙子": Element.WATER, "丁丑": Element.WATER,
    "戊寅": Element.EARTH, "己卯": Element.EARTH,
    "庚辰": Element.EARTH, "辛巳": Element.EARTH,
    "壬午": Element.FIRE, "癸未": Element.FIRE,
    "甲申": Element.METAL, "乙酉": Element.METAL,
    "丙戌": Element.EARTH, "丁亥": Element.EARTH,
    "戊子": Element.EARTH, "己丑": Element.EARTH,
    "庚寅": Element.METAL, "辛卯": Element.METAL,
    "壬辰": Element.WATER, "癸巳": Element.WATER,
    "甲午": Element.WOOD, "乙未": Element.WOOD,
    "丙申": Element.FIRE, "丁酉": Element.FIRE,
    "戊戌": Element.EARTH, "己亥": Element.EARTH,
    "庚子": Element.METAL, "辛丑": Element.METAL,
    "壬寅": Element.WATER, "癸卯": Element.WATER,
    "甲辰": Element.WOOD, "乙巳": Element.WOOD,
    "丙午": Element.FIRE, "丁未": Element.FIRE,
    "戊申": Element.EARTH, "己酉": Element.EARTH,
    "庚戌": Element.EARTH, "辛亥": Element.EARTH,
}

# 二十四节气日期范围 (大致)
SOLAR_TERMS_DATES = {
    SolarTerm.XIAOHAN: (1, 5, 7),
    SolarTerm.DAHAN: (1, 20, 21),
    SolarTerm.LICHUN: (2, 3, 5),
    SolarTerm.JINGZHE: (3, 5, 7),
    SolarTerm.CHUNFEN: (3, 20, 22),
    SolarTerm.QINGMING: (4, 4, 6),
    SolarTerm.GUYU: (4, 19, 21),
    SolarTerm.LIXIA: (5, 5, 7),
    SolarTerm.XIAOMAN: (5, 20, 22),
    SolarTerm.MANGZHONG: (6, 5, 7),
    SolarTerm.XIAZHI: (6, 20, 22),
    SolarTerm.XIAOSHU: (7, 6, 8),
    SolarTerm.DASHU: (7, 22, 24),
    SolarTerm.LIQIU: (8, 7, 9),
    SolarTerm.CHUSHU: (8, 22, 24),
    SolarTerm.QIUFEN: (9, 22, 24),
    SolarTerm.SHUANGJIANG: (10, 23, 24),
    SolarTerm.LIDONG: (11, 7, 8),
    SolarTerm.XIAOXUE: (11, 22, 23),
    SolarTerm.DAXUE: (12, 6, 8),
}


class ChineseCalendarEngine:
    """中国农历日历计算引擎"""
    
    def __init__(self):
        if Converter is None:
            raise RuntimeError(
                "lunarcalendar library not installed. "
                "Install with: pip install lunarcalendar"
            )
        self._solar_term_cache: Dict[int, Tuple[datetime, SolarTerm]] = {}
    
    def get_lunar_date(self, dt: datetime) -> Dict[str, any]:
        """
        获取指定日期的农历信息
        
        Args:
            dt: 公历日期
            
        Returns:
            {
                'lunar_date': '五月初五',
                'lunar_year': 2026,
                'lunar_month': 5,
                'lunar_day': 5,
                'zodiac_animal': '龙',
                'solar_term': '芒种',
                'days_to_next_solar_term': 13,
                'is_leap_month': False,
            }
        """
        try:
            solar = Solar(dt.year, dt.month, dt.day)
            lunar = Converter.Solar2Lunar(solar)
            
            # 获取农历日期显示名称
            lunar_date_str = self._format_lunar_date(lunar)
            
            # 获取生肖
            zodiac = self._get_zodiac_animal(lunar.year)
            
            # 获取当前/最近的节气
            solar_term, days_to_next = self._get_nearest_solar_term(dt)
            
            return {
                'lunar_date': lunar_date_str,
                'lunar_year': lunar.year,
                'lunar_month': lunar.month,
                'lunar_day': lunar.day,
                'zodiac_animal': zodiac.value,
                'solar_term': solar_term.value if solar_term else None,
                'days_to_next_solar_term': days_to_next,
                'is_leap_month': lunar.isleap,
            }
        except Exception as e:
            logger.error(f"Failed to get lunar date for {dt}: {e}")
            return {}
    
    def get_solar_terms_this_month(self, dt: Optional[datetime] = None) -> List[Dict]:
        """
        获取本月的所有节气
        
        Args:
            dt: 指定日期（默认为今天）
            
        Returns:
            [
                {
                    'date': '2026-06-05',
                    'name': '芒种',
                    'lunar_date': '五月初一',
                    'impact': 'market_activity_increase',
                },
                ...
            ]
        """
        if dt is None:
            dt = datetime.now()
        
        terms_this_month = []
        current_year = dt.year
        current_month = dt.month
        
        for term, (month, start_day, end_day) in SOLAR_TERMS_DATES.items():
            if month == current_month:
                # 创建该节气的日期 (取中间值作为估计)
                estimated_day = (start_day + end_day) // 2
                term_date = datetime(current_year, month, estimated_day)
                
                # 获取农历日期
                lunar_date = self._format_lunar_date_for_datetime(term_date)
                
                terms_this_month.append({
                    'date': term_date.strftime('%Y-%m-%d'),
                    'name': term.value,
                    'lunar_date': lunar_date,
                    'impact': self._get_solar_term_market_impact(term),
                })
        
        return sorted(terms_this_month, key=lambda x: x['date'])
    
    def get_solar_terms_this_year(self, year: Optional[int] = None) -> Dict[str, List[Dict]]:
        """
        获取全年的所有节气
        
        Returns:
            {
                '一月': [{'date': '2026-01-05', 'name': '小寒', ...}],
                '二月': [...],
                ...
            }
        """
        if year is None:
            year = datetime.now().year
        
        month_names = [
            '一月', '二月', '三月', '四月', '五月', '六月',
            '七月', '八月', '九月', '十月', '十一月', '十二月'
        ]
        
        result = {name: [] for name in month_names}
        
        for term, (month, start_day, end_day) in SOLAR_TERMS_DATES.items():
            estimated_day = (start_day + end_day) // 2
            term_date = datetime(year, month, estimated_day)
            lunar_date = self._format_lunar_date_for_datetime(term_date)
            
            result[month_names[month - 1]].append({
                'date': term_date.strftime('%Y-%m-%d'),
                'name': term.value,
                'lunar_date': lunar_date,
                'impact': self._get_solar_term_market_impact(term),
            })
        
        return result
    
    def get_element_by_date(self, dt: datetime) -> Dict[str, str]:
        """
        根据日期获取五行纳音属性
        
        Args:
            dt: 日期
            
        Returns:
            {
                'element': '金',
                'yin_yang': '阳',
                'nayin_element': '金',
                'heavenly_stem': '庚',
                'earthly_branch': '午',
                'meaning': '路旁土',  # 纳音含义
            }
        """
        try:
            # 计算干支序数
            # 基准: 2000年1月1日是 庚辰 日
            base_date = datetime(2000, 1, 1)  # 庚辰
            days_diff = (dt - base_date).days
            
            # 天干 (10年一轮) 和 地支 (12年一轮) 是独立的
            stem_index = (days_diff + 8) % 10  # 2000年1月1日是第9个天干
            branch_index = (days_diff + 4) % 12  # 2000年1月1日是第5个地支
            
            heavenly_stem = HEAVENLY_STEMS[stem_index]
            earthly_branch = EARTHLY_BRANCHES[branch_index]
            sexagenary = f"{heavenly_stem}{earthly_branch}"
            
            # 获取五行
            stem_element = HEAVENLY_STEM_ELEMENTS[heavenly_stem]
            branch_element = EARTHLY_BRANCH_ELEMENTS[earthly_branch]
            nayin_element = NAYIN_ELEMENTS.get(sexagenary, Element.EARTH)
            
            # 确定阴阳
            yin_yang = YinYang.YANG if stem_index % 2 == 0 else YinYang.YIN
            
            return {
                'element': stem_element.value,
                'yin_yang': yin_yang.value,
                'nayin_element': nayin_element.value,
                'heavenly_stem': heavenly_stem,
                'earthly_branch': earthly_branch,
                'sexagenary_cycle': sexagenary,
            }
        except Exception as e:
            logger.error(f"Failed to get element by date {dt}: {e}")
            return {}
    
    def get_fortune_calendar(
        self,
        year_month: str,  # 格式: '2026-06'
    ) -> List[Dict]:
        """
        获取指定月份的吉凶日历
        
        Args:
            year_month: 'YYYY-MM'
            
        Returns:
            [
                {
                    'date': '2026-06-01',
                    'lunar_date': '四月廿五',
                    'fortune_level': 8,        # 1-10
                    'heavenly_stem': '庚',
                    'earthly_branch': '午',
                    'recommendation': '适合交易，建议加仓',
                    'avoid': ['婚礼', '搬家'],
                },
                ...
            ]
        """
        try:
            year, month = map(int, year_month.split('-'))
            
            # 获取该月有多少天
            if month == 12:
                next_month_first = datetime(year + 1, 1, 1)
            else:
                next_month_first = datetime(year, month + 1, 1)
            
            last_day = (next_month_first - timedelta(days=1)).day
            
            calendar = []
            for day in range(1, last_day + 1):
                dt = datetime(year, month, day)
                
                # 获取农历和五行
                lunar_info = self.get_lunar_date(dt)
                element_info = self.get_element_by_date(dt)
                
                # 计算吉凶指数
                fortune_level = self._calculate_fortune_level(element_info, lunar_info)
                
                # 获取建议
                recommendation, avoid = self._get_day_recommendation(
                    fortune_level,
                    element_info,
                    lunar_info
                )
                
                calendar.append({
                    'date': dt.strftime('%Y-%m-%d'),
                    'lunar_date': lunar_info.get('lunar_date', ''),
                    'fortune_level': fortune_level,
                    'heavenly_stem': element_info.get('heavenly_stem', ''),
                    'earthly_branch': element_info.get('earthly_branch', ''),
                    'sexagenary_cycle': element_info.get('sexagenary_cycle', ''),
                    'element': element_info.get('element', ''),
                    'recommendation': recommendation,
                    'avoid': avoid,
                })
            
            return calendar
        except Exception as e:
            logger.error(f"Failed to get fortune calendar for {year_month}: {e}")
            return []
    
    def get_zodiac_year_fortune(self, year: int) -> Dict[str, any]:
        """
        获取某个生肖年的整体运势
        
        Args:
            year: 公历年份
            
        Returns:
            {
                'year': 2026,
                'zodiac': '龙',
                'earthly_branch': '辰',
                'element': '土',
                'description': '龙年运势详解',
                'fortune_trend': 'positive',
            }
        """
        try:
            # 计算该年的生肖
            zodiac = self._get_zodiac_animal(year)
            
            # 计算该年的天干地支
            year_stem_index = (year - 1900 + 6) % 10
            year_branch_index = (year - 1900) % 12
            
            stem = HEAVENLY_STEMS[year_stem_index]
            branch = EARTHLY_BRANCHES[year_branch_index]
            
            stem_element = HEAVENLY_STEM_ELEMENTS[stem]
            branch_element = EARTHLY_BRANCH_ELEMENTS[branch]
            
            return {
                'year': year,
                'zodiac': zodiac.value,
                'heavenly_stem': stem,
                'earthly_branch': branch,
                'stem_element': stem_element.value,
                'branch_element': branch_element.value,
                'fortune_trend': self._get_year_fortune_trend(year),
                'description': f"{zodiac.value}年，{stem}{branch}年...",
            }
        except Exception as e:
            logger.error(f"Failed to get zodiac year fortune for {year}: {e}")
            return {}
    
    # ============ 辅助方法 ============
    
    @staticmethod
    def _format_lunar_date(lunar) -> str:
        """格式化农历日期为中文文本"""
        lunar_months = [
            '正', '二', '三', '四', '五', '六',
            '七', '八', '九', '十', '冬', '腊'
        ]
        lunar_days = [
            '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
            '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
            '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'
        ]
        
        month_name = lunar_months[lunar.month - 1]
        if lunar.isleap:
            month_name = "闰" + month_name
        
        day_name = lunar_days[lunar.day - 1]
        
        return f"{month_name}{day_name}"
    
    @staticmethod
    def _format_lunar_date_for_datetime(dt: datetime) -> str:
        """从datetime对象获取农历日期文本"""
        try:
            solar = Solar(dt.year, dt.month, dt.day)
            lunar = Converter.Solar2Lunar(solar)
            return ChineseCalendarEngine._format_lunar_date(lunar)
        except:
            return ""
    
    @staticmethod
    def _get_zodiac_animal(year: int) -> ZodiacAnimal:
        """根据年份获取生肖"""
        zodiac_index = (year - 1900) % 12
        return ZodiacAnimal(list(ZodiacAnimal)[zodiac_index])
    
    @staticmethod
    def _get_nearest_solar_term(dt: datetime) -> Tuple[Optional[SolarTerm], int]:
        """获取最接近的节气及距离"""
        current_month = dt.month
        current_day = dt.day
        
        # 查找本月及下月的节气
        nearest_term = None
        min_days = float('inf')
        
        for month in [current_month, (current_month % 12) + 1]:
            for term, (m, start, end) in SOLAR_TERMS_DATES.items():
                if m == month:
                    estimated_day = (start + end) // 2
                    term_date = datetime(dt.year, month, estimated_day)
                    days_diff = (term_date - dt).days
                    
                    if 0 <= days_diff < min_days:
                        min_days = days_diff
                        nearest_term = term
        
        return nearest_term, max(0, min_days)
    
    @staticmethod
    def _get_solar_term_market_impact(term: SolarTerm) -> str:
        """获取节气对市场的影响标签"""
        # 节气与市场情绪的关系 (基于历史规律)
        impact_map = {
            SolarTerm.LICHUN: "market_awakening",      # 春风复苏
            SolarTerm.JINGZHE: "market_activity_increase",
            SolarTerm.CHUNFEN: "peak_sentiment",
            SolarTerm.LIXIA: "summer_transition",
            SolarTerm.XIAOMAN: "market_harvest",
            SolarTerm.MANGZHONG: "high_activity",
            SolarTerm.XIAZHI: "peak_sentiment_caution",
            SolarTerm.LIQIU: "market_shift",
            SolarTerm.QIUFEN: "balance_correction",
            SolarTerm.LIDONG: "winter_decline",
            SolarTerm.XIAOXUE: "market_decline",
            SolarTerm.DAXUE: "near_bottom",
        }
        return impact_map.get(term, "neutral")
    
    @staticmethod
    def _calculate_fortune_level(element_info: Dict, lunar_info: Dict) -> int:
        """
        计算日期吉凶等级 (1-10)
        
        基于:
        - 天干地支相克程度
        - 农历日期 (初一、十五 通常较吉)
        """
        fortune = 5  # 基础中性值
        
        # 农历初一、十五通常较吉
        lunar_day = lunar_info.get('lunar_day', 15)
        if lunar_day in [1, 15]:
            fortune += 2
        elif lunar_day in [2, 16]:
            fortune += 1
        
        # 根据五行生克调整
        element = element_info.get('element', '木')
        yin_yang = element_info.get('yin_yang', '阳')
        
        # 这是简化版本，实际应用中需要更复杂的算法
        if yin_yang == '阳':
            fortune += 1
        
        return min(10, max(1, fortune))
    
    @staticmethod
    def _get_day_recommendation(
        fortune_level: int,
        element_info: Dict,
        lunar_info: Dict,
    ) -> Tuple[str, List[str]]:
        """
        根据吉凶等级获取交易建议
        
        Returns:
            (推荐文本, 避免事项列表)
        """
        if fortune_level >= 8:
            return "🟢 吉日，适合交易和加仓", []
        elif fortune_level >= 6:
            return "🟡 中吉，可正常交易", ["大幅加仓"]
        elif fortune_level >= 4:
            return "🟡 中平，建议观望", ["新仓", "追高"]
        else:
            return "🔴 凶日，建议回避", ["任何新交易", "加仓"]
    
    @staticmethod
    def _get_year_fortune_trend(year: int) -> str:
        """
        获取该年的整体运势趋势
        基于天干地支的生克关系
        """
        year_branch_index = (year - 1900) % 12
        
        # 简化版本：某些地支年份通常为上升年
        strong_years = [4, 8, 0]  # 龙年、猴年、鼠年通常较强
        
        if year_branch_index in strong_years:
            return "strong_positive"
        else:
            return "neutral"


# 全局单例
_calendar_engine_instance: Optional[ChineseCalendarEngine] = None


def get_calendar_engine() -> ChineseCalendarEngine:
    """获取全局日历引擎实例"""
    global _calendar_engine_instance
    if _calendar_engine_instance is None:
        _calendar_engine_instance = ChineseCalendarEngine()
    return _calendar_engine_instance
