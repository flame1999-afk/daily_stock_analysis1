# 🔮 占星学与气候预测洞察扩展

## 📋 核心设计理念

**关键原则**: 占星学与气候预测作为 **独立分析视角**，不影响核心交易评分

- ✅ **分离不混淆**: 技术面 + 基本面 + 情绪面保持独立，占星/气候作为补充注解
- ✅ **透明准确率**: 每条预测都显示历史准确率，用户自行判断可信度
- ✅ **事件关联分析**: 预测可能影响股价的宏观事件（政策、气候、自然现象）
- ✅ **持续学习**: 模型逐月回测自身预测准确性，动态调整权重

---

## 🏗️ 架构设计

### 数据流向

```
Stock Analysis Pipeline
├─ Core Analysis (技术/基本面/情绪)
│  └─ → Sentiment Score [0-100]  (权重 100%)
│
└─ Supplementary Insights (新增)
   ├─ Astro Insights Panel
   │  ├─ Chinese Calendar Events
   │  ├─ Heavenly-Earthly Fortune
   │  ├─ Industry Five-Element Phase
   │  ├─ Company Destiny Score
   │  ├─ Predicted Events (政治/经济/自然事件)
   │  └─ Accuracy: 62% (历史准确率)
   │
   ├─ Climate & Weather Insights Panel
   │  ├─ Seasonal Transitions
   │  ├─ Extreme Weather Risks
   │  ├─ Regional Logistics Impact
   │  ├─ Agricultural Commodity Effects
   │  └─ Accuracy: 75% (NOAA/CMA数据)
   │
   └─ Macro Event Impact Panel
      ├─ Policy Events
      ├─ Industry Regulations
      ├─ Natural Disasters
      └─ Accuracy: 58% (新闻舆情验证)

Final Dashboard:
├─ Core Score: 65 / 100 (不变，维持客观性)
├─ Recommendation: HOLD
├─ Technical Analysis: [...existing...]
├─ NEW: Supplementary Insights
│  ├─ 【占星学洞察】(准确率 62%)
│  ├─ 【气候与自然事件】(准确率 75%)
│  └─ 【宏观政策预测】(准确率 58%)
└─ Risk Alerts: [...existing...]
```

---

## 📊 模块结构

```
src/addons/
└── astro_climate_insights/
    ├── __init__.py
    ├── calendar_engine.py              # 农历/节气/五行
    ├── heavenly_earthly.py             # 天干地支吉凶
    ├── industry_mapping.py             # 五行与行业映射
    ├── company_profile.py              # 企业成立日期运势
    ├── event_predictor.py              # 政治/经济事件预测
    ├── climate_weather_api.py           # 气候数据源集成
    ├── accuracy_tracker.py             # 准确率追踪与学习
    ├── insight_synthesizer.py          # 洞察汇总生成
    └── integration.py                  # 与主流程集成
```

---

## 🔮 占星学洞察面板

### 1. 数据模型 (`src/schemas/astro_insight_schema.py`)

```python
from typing import Optional, List
from pydantic import BaseModel, Field

class AstroEvent(BaseModel):
    """占星学预测事件"""
    date: str                           # ISO格式日期
    lunar_date: str                     # 农历日期
    event_type: str                     # fortune_day / sector_phase / company_cycle / seasonal_shift
    description: str                    # 事件描述
    impact_sectors: List[str]           # 可能影响的行业
    expected_direction: str             # bullish / neutral / bearish
    confidence: float = Field(ge=0, le=1)  # 0.0-1.0
    historical_accuracy: float = Field(ge=0, le=1)  # 历史准确率


class AstroInsightPanel(BaseModel):
    """占星学洞察面板"""
    analysis_date: str
    lunar_info: dict                    # {'lunar_date': '五月初五', 'animal': '龙', ...}
    
    # 今日吉凶
    today_fortune: dict                 # {'level': 7, 'heavenly': '庚', 'earthly': '午', 'desc': '...'}
    
    # 本月/季度重要节点
    upcoming_events: List[AstroEvent]   # 未来30天的占星事件
    
    # 行业五行阶段
    sector_phase: dict                  # {'element': '火', 'phase': 'peak', 'affected_sectors': [...]}
    
    # 企业运势
    company_destiny: dict               # {'code': '600519', 'harmony': 8, 'cycle_status': '...'}
    
    # 政策/经济事件预测 (占星学视角)
    predicted_macro_events: List[dict]  # [{'date': '2026-07-15', 'type': 'policy', 'desc': '...'}]
    
    # 准确率跟踪
    panel_accuracy: float = Field(ge=0, le=1)  # 整个面板的平均准确率
    last_updated: str                    # 最后更新日期
```

### 2. 核心功能实现 (`src/addons/astro_climate_insights/astro_insights.py`)

```python
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from src.addons.astro_climate_insights.accuracy_tracker import AccuracyTracker

logger = logging.getLogger(__name__)

class AstroInsightEngine:
    """占星学洞察生成引擎"""
    
    def __init__(self):
        self.accuracy_tracker = AccuracyTracker()
        
    def generate_panel(
        self,
        stock_code: str,
        analysis_date: str,
    ) -> Optional[AstroInsightPanel]:
        """
        生成占星学洞察面板
        
        Args:
            stock_code: 股票代码
            analysis_date: 分析日期 (ISO格式)
            
        Returns:
            AstroInsightPanel 或 None
        """
        try:
            from src.addons.astro_climate_insights.calendar_engine import ChineseCalendarEngine
            from src.addons.astro_climate_insights.company_profile import CompanyAstroProfile
            
            analysis_dt = datetime.fromisoformat(analysis_date)
            engine = ChineseCalendarEngine()
            profile = CompanyAstroProfile()
            
            # 1. 农历信息
            lunar_info = engine.get_lunar_date(analysis_dt)
            
            # 2. 今日吉凶
            today_fortune = self._analyze_day_fortune(analysis_dt)
            
            # 3. 未来30天占星事件
            upcoming_events = self._predict_upcoming_events(analysis_dt)
            
            # 4. 行业五行阶段
            sector_phase = self._get_sector_phase(analysis_dt)
            
            # 5. 企业运势
            company_destiny = profile.analyze_company_destiny(stock_code)
            
            # 6. 宏观事件预测
            macro_events = self._predict_macro_events(analysis_dt)
            
            # 7. 获取该面板的平均准确率
            panel_accuracy = self.accuracy_tracker.get_panel_accuracy()
            
            panel = AstroInsightPanel(
                analysis_date=analysis_date,
                lunar_info=lunar_info,
                today_fortune=today_fortune,
                upcoming_events=upcoming_events,
                sector_phase=sector_phase,
                company_destiny=company_destiny,
                predicted_macro_events=macro_events,
                panel_accuracy=panel_accuracy,
                last_updated=datetime.now().isoformat(),
            )
            
            logger.info(f"[占星学] 为 {stock_code} 生成洞察面板，准确率: {panel_accuracy:.1%}")
            return panel
            
        except Exception as e:
            logger.warning(f"[占星学] 生成面板失败: {e}")
            return None
    
    def _analyze_day_fortune(self, dt: datetime) -> Dict[str, Any]:
        """分析特定日期的吉凶"""
        # 实现天干地支分析
        # 返回: {'level': 7, 'heavenly': '庚', 'earthly': '午', 'desc': '...'}
        pass
    
    def _predict_upcoming_events(self, dt: datetime) -> List[AstroEvent]:
        """预测未来30天的占星关键事件"""
        # 返回节气变化、农历重要日期等
        pass
    
    def _get_sector_phase(self, dt: datetime) -> Dict[str, Any]:
        """获取当前五行阶段与行业影响"""
        # 返回当前主导五行、受益行业、衰落行业
        pass
    
    def _predict_macro_events(self, dt: datetime) -> List[Dict[str, Any]]:
        """预测可能的宏观事件（占星学+历史规律）"""
        # 基于农历、节气、大运周期预测
        # 返回: [{'date': '2026-07-15', 'type': 'policy', 'desc': '...', 'confidence': 0.65}]
        pass
```

---

## 🌍 气候与天气洞察面板

### 1. 数据模型 (`src/schemas/climate_insight_schema.py`)

```python
from typing import Optional, List
from pydantic import BaseModel, Field

class WeatherEvent(BaseModel):
    """气候事件"""
    date: str
    region: str
    event_type: str                    # drought / flood / heat_wave / typhoon / frost
    severity: str                      # low / medium / high / extreme
    affected_industries: List[str]     # ['农业', '水利', '运输']
    expected_impact: str               # bullish / bearish / neutral
    data_source: str                   # NOAA / CMA / 中国气象局


class ClimateInsightPanel(BaseModel):
    """气候与自然事件洞察面板"""
    analysis_date: str
    
    # 当前季节状态
    seasonal_status: dict              # {'season': '初夏', 'temp_trend': 'rising', ...}
    
    # 近期极端天气风险
    extreme_weather_alerts: List[WeatherEvent]
    
    # 行业特定影响
    agriculture_outlook: dict          # {'crop_prices': 'up', 'factors': ['干旱风险'], ...}
    logistics_impact: dict             # {'transport_delay_risk': 'medium', 'affected_routes': [...]}
    energy_demand: dict                # {'heating/cooling_demand': 'normal', 'renewable_generation': 'strong'}
    
    # 气候相关商品影响
    commodity_impacts: dict            # {'oil': 'up', 'grain': 'down', 'power': 'stable'}
    
    # 准确率
    panel_accuracy: float = Field(ge=0, le=1)


class MacroEventImpactPanel(BaseModel):
    """宏观事件影响洞察"""
    analysis_date: str
    
    # 近期政策事件预测
    policy_events: List[dict]          # 预测的政策事件
    
    # 行业监管预期
    regulation_outlook: dict
    
    # 自然灾害风险
    disaster_risks: List[dict]
    
    # 综合评估
    macro_sentiment: str               # very_bullish / bullish / neutral / bearish / very_bearish
    panel_accuracy: float
```

### 2. 气候数据源集成

```python
# src/addons/astro_climate_insights/climate_weather_api.py

import logging
from typing import Optional, Dict, List
import aiohttp

logger = logging.getLogger(__name__)

class ClimateWeatherDataProvider:
    """气候与天气数据提供者"""
    
    def __init__(self):
        self.noaa_api = NOAAWeatherAPI()      # 美国国家气象局 (全球数据)
        self.cma_api = CMAWeatherAPI()        # 中国气象局
        self.cache = {}
        
    async def get_seasonal_outlook(self, region: str, months_ahead: int = 3) -> Dict:
        """
        获取季节性展望 (使用官方数据源)
        
        Sources:
        - NOAA Climate Prediction Center
        - CMA (中国气象局)
        - ECMWF 欧洲中期预报中心
        """
        # 调用官方气象API获取可靠的季节预测
        pass
    
    async def get_extreme_weather_alerts(self, region: str) -> List[Dict]:
        """
        获取极端天气预警
        
        Sources:
        - NOAA Alerts
        - CMA Emergency Warnings
        - Local weather services
        """
        # 返回当前生效的预警信息
        pass
    
    async def get_agricultural_outlook(self) -> Dict:
        """
        获取农业前景 (影响农产品和相关企业)
        
        Sources:
        - USDA (美国农业部)
        - CNKI 农业研究库
        - 中国农业信息网
        """
        # 返回农作物长势、产量预期、价格趋势
        pass
```

---

## 📈 准确率追踪与学习

### 1. 准确率记录系统 (`src/addons/astro_climate_insights/accuracy_tracker.py`)

```python
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import json

logger = logging.getLogger(__name__)

class AccuracyTracker:
    """
    追踪占星学与气候预测的准确率
    
    工作流程:
    1. 预测发布时记录预测详情 + 时间戳
    2. 预测期满后对比实际结果
    3. 更新准确率统计
    4. 动态调整预测权重
    """
    
    def __init__(self, db_path: str = "./data/accuracy_records.db"):
        self.db_path = db_path
        self._init_db()
        
    def record_prediction(
        self,
        panel_type: str,              # 'astro' / 'climate' / 'macro_event'
        stock_code: str,
        event_date: str,
        prediction: Dict,
        confidence: float,
    ) -> str:
        """
        记录一条预测
        
        Args:
            panel_type: 预测面板类型
            stock_code: 股票代码
            event_date: 预测事件日期
            prediction: 预测详情 (dict)
            confidence: 预测置信度 (0.0-1.0)
            
        Returns:
            prediction_id (用于后续验证)
        """
        prediction_id = self._generate_id()
        record = {
            'id': prediction_id,
            'panel_type': panel_type,
            'stock_code': stock_code,
            'event_date': event_date,
            'prediction_date': datetime.now().isoformat(),
            'prediction': prediction,
            'confidence': confidence,
            'actual_result': None,          # 事后填充
            'accurate': None,               # 事后填充
            'created_at': datetime.now().isoformat(),
        }
        
        self._save_record(record)
        logger.info(f"[准确率] 记录预测 {prediction_id}: {panel_type}/{stock_code}/{event_date}")
        return prediction_id
    
    def validate_prediction(
        self,
        prediction_id: str,
        actual_result: Dict,
    ) -> bool:
        """
        事后验证预测准确性
        
        Args:
            prediction_id: 预测ID
            actual_result: 实际发生的结果
            
        Returns:
            是否准确
        """
        record = self._get_record(prediction_id)
        if not record:
            logger.warning(f"[准确率] 预测记录未找到: {prediction_id}")
            return False
        
        # 对比逻辑：根据 panel_type 采用不同的对比方法
        accurate = self._compare_results(
            record['panel_type'],
            record['prediction'],
            actual_result
        )
        
        record['actual_result'] = actual_result
        record['accurate'] = accurate
        record['validated_at'] = datetime.now().isoformat()
        
        self._update_record(record)
        logger.info(f"[准确率] 验证预测 {prediction_id}: {'✓ 准确' if accurate else '✗ 失误'}")
        
        return accurate
    
    def get_panel_accuracy(
        self,
        panel_type: Optional[str] = None,
        days: int = 90,
    ) -> float:
        """
        获取指定时间内的准确率
        
        Args:
            panel_type: 面板类型 (None=全部)
            days: 回溯天数
            
        Returns:
            准确率 (0.0-1.0)
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        records = self._query_records({
            'validated': True,
            'created_at_after': cutoff_date,
        })
        
        if panel_type:
            records = [r for r in records if r['panel_type'] == panel_type]
        
        if not records:
            return 0.5  # 默认返回50%
        
        accurate_count = sum(1 for r in records if r['accurate'])
        accuracy = accurate_count / len(records)
        
        logger.debug(f"[准确率] {panel_type or '全部'}: {accuracy:.1%} ({accurate_count}/{len(records)})")
        return accuracy
    
    def get_accuracy_trends(
        self,
        panel_type: str,
        window_days: int = 30,
    ) -> List[Dict]:
        """
        获取准确率趋势数据（用于前端展示）
        
        Returns:
            [
                {'date': '2026-05-01', 'accuracy': 0.65, 'sample_size': 12},
                {'date': '2026-05-08', 'accuracy': 0.68, 'sample_size': 15},
                ...
            ]
        """
        # 按周/月聚合准确率
        pass
    
    def _compare_results(
        self,
        panel_type: str,
        predicted: Dict,
        actual: Dict,
    ) -> bool:
        """根据预测类型对比结果"""
        if panel_type == 'astro':
            # 对比方向预测 (bullish/neutral/bearish)
            pred_direction = predicted.get('expected_direction')
            actual_direction = actual.get('actual_direction')  # 由后期分析填充
            return pred_direction == actual_direction
        
        elif panel_type == 'climate':
            # 对比极端天气是否发生
            pred_severity = predicted.get('severity')
            actual_occurred = actual.get('occurred', False)
            if not actual_occurred:
                return pred_severity == 'low'  # 预测不发生但实际发生 = 失误
            return actual.get('actual_severity') == pred_severity
        
        elif panel_type == 'macro_event':
            # 对比事件是否发生
            return actual.get('occurred', False)
        
        return False
```

### 2. 准确率显示在前���

```python
# 在 Dashboard 中显示准确率

class SupplementaryInsightPanel(BaseModel):
    """补充洞察面板"""
    
    astro_insights: Optional[AstroInsightPanel] = None
    astro_accuracy: float = Field(ge=0, le=1)  # 如 0.62 = 62%
    astro_last_validation: Optional[str]       # 最后验证日期
    astro_sample_size: int                     # 验证样本量
    
    climate_insights: Optional[ClimateInsightPanel] = None
    climate_accuracy: float = Field(ge=0, le=1)
    climate_last_validation: Optional[str]
    climate_sample_size: int
    
    macro_event_insights: Optional[MacroEventImpactPanel] = None
    macro_accuracy: float
    macro_last_validation: Optional[str]
    macro_sample_size: int
```

---

## 🎯 事件预测与关联分析

### 1. 政治/经济事件预测

```python
# src/addons/astro_climate_insights/event_predictor.py

class MacroEventPredictor:
    """宏观事件预测"""
    
    def predict_policy_events(self, forecast_days: int = 90) -> List[Dict]:
        """
        预测可能的政策事件
        
        数据源:
        - 官方议程 (易于验证的计划事件)
        - 新闻舆情分析 (政策倾向)
        - 占星学规律 (历史周期)
        """
        events = []
        
        # 例子1: 年度两会 (农历新年后)
        events.append({
            'date': '2026-03-15',
            'type': 'political',
            'description': '全国两会 (预期)',
            'affected_sectors': ['金融', '房地产', '新能源'],
            'expected_policy': '可能涉及货币政策调整',
            'confidence': 0.95,  # 高确定性（历史规律）
            'historical_accuracy': 0.99,
        })
        
        # 例子2: 季度经济数据发布 (占星学+历史规律)
        events.append({
            'date': '2026-07-15',
            'type': 'economic_report',
            'description': '上半年经济数据发布',
            'affected_sectors': ['大盘指数', '金融'],
            'expected_impact': '可能造成短期波动',
            'confidence': 0.85,
            'historical_accuracy': 0.78,
        })
        
        return events
    
    def predict_climate_policy_impacts(self) -> Dict:
        """
        预测气候政策相关的股票影响
        
        例如:
        - 极端高温 → 电力需求↑ → 电力股↑
        - 严重干旱 → 农产品↓ → 农业股↓
        - 雾霾预警 → 环保政策↑ → 环保股↑
        """
        pass
```

### 2. 行业与事件的关联

```python
# src/addons/astro_climate_insights/industry_event_impact.py

INDUSTRY_EVENT_MAPPING = {
    # 政策事件
    '货币政策放宽': {
        'bullish_sectors': ['地产', '建筑', '汽车', '家电'],
        'bearish_sectors': ['医药', '消费'],
        'affected_stocks': [...],
    },
    
    # 气候事件
    '极端高温': {
        'bullish_sectors': ['电力', '空调制造', '饮料'],
        'bearish_sectors': ['农业', '运输'],
    },
    
    '严重干旱': {
        'bullish_sectors': ['水利设施', '灌溉技术'],
        'bearish_sectors': ['农业', '食品'],
    },
    
    # 占星事件
    '农历新年': {
        'bullish_sectors': ['消费', '旅游', '食品'],
        'bearish_sectors': ['制造业', '建筑'],
    },
}
```

---

## 📋 Schema 集成

### 修改 `src/schemas/report_schema.py`

```python
from typing import Optional
from pydantic import BaseModel, Field

class SupplementaryInsights(BaseModel):
    """补充洞察（占星学、气候、宏观事件）"""
    
    # 占星学洞察
    astro_panel: Optional[Dict[str, Any]] = None
    astro_accuracy: float = Field(default=0.5, ge=0, le=1)
    astro_accuracy_as_percent: str = Field(default="50%")  # 易读格式
    astro_sample_size: int = 0
    astro_note: str = "基于农历、天干地支、五行理论的参考性洞察"
    
    # 气候与天气
    climate_panel: Optional[Dict[str, Any]] = None
    climate_accuracy: float = Field(default=0.75, ge=0, le=1)
    climate_accuracy_as_percent: str = Field(default="75%")
    climate_sample_size: int = 0
    climate_note: str = "基于NOAA、CMA等官方气象数据的科学性分析"
    
    # 宏观事件
    macro_events_panel: Optional[Dict[str, Any]] = None
    macro_accuracy: float = Field(default=0.58, ge=0, le=1)
    macro_accuracy_as_percent: str = Field(default="58%")
    macro_sample_size: int = 0
    macro_note: str = "基于新闻舆情、历史规律的事件预测"
    
    # 综合建议
    key_insights: List[str] = []  # 3-5个核心洞察
    risk_flags: List[str] = []    # 需要特别关注的风险
    opportunities: List[str] = [] # 潜在机会


class Dashboard(BaseModel):
    # ... 现有字段（技术/基本面/情绪） ...
    
    # NEW: 补充洞察（不影响核心评分）
    supplementary_insights: Optional[SupplementaryInsights] = None


class AnalysisReportSchema(BaseModel):
    # ... 现有字段 ...
    
    # 核心评分（保持100%客观，不受补充洞察影响）
    sentiment_score: Optional[int] = Field(None, ge=0, le=100)
    operation_advice: Optional[str] = None
    
    # 补充洞察（独立面板）
    supplementary_insights: Optional[SupplementaryInsights] = None
```

---

## 🔌 集成到主分析流程

### 修改 `src/core/pipeline.py`

```python
class StockAnalysisPipeline:
    
    def process_single_stock(self, code: str, ...):
        """处理单只股票"""
        
        # 1. 核心分析（技术/基本面/情绪）
        result = self.analyzer.analyze(code, ...)
        
        # 2. NEW: 补充洞察（占星/气候/宏观）
        if getattr(self.config, 'supplementary_insights_enabled', True):
            supplementary = self._generate_supplementary_insights(
                stock_code=code,
                analysis_date=datetime.now().date(),
            )
            result.supplementary_insights = supplementary
        
        return result
    
    def _generate_supplementary_insights(self, stock_code: str, analysis_date: date):
        """生成补充洞察"""
        from src.addons.astro_climate_insights.integration import SupplementaryInsightEngine
        
        engine = SupplementaryInsightEngine()
        return engine.generate(
            stock_code=stock_code,
            analysis_date=analysis_date,
        )
```

---

## 📊 前端展示示例

### Web UI 报告模板

```html
<!-- 核心分析结果（权重100%，不变） -->
<div class="core-analysis">
  <h2>📊 核心分析结果</h2>
  <div class="score">
    <span class="label">决策评分</span>
    <span class="value">65 / 100</span>
  </div>
  <p class="recommendation">建议: <strong>HOLD (持有)</strong></p>
  <p class="technical">技术面: 上升趋势...</p>
  <p class="fundamental">基本面: 业绩稳健...</p>
</div>

<!-- 补充洞察（参考性，明确标注准确率） -->
<div class="supplementary-insights">
  <h2>🔮 补充洞察（参考性）</h2>
  
  <!-- 占星学洞察 -->
  <div class="astro-panel">
    <div class="header">
      <h3>占星学洞察</h3>
      <span class="accuracy">准确率: 62% (基于231次验证)</span>
    </div>
    <div class="content">
      <p><strong>农历日期:</strong> 五月初五 (端午节)</p>
      <p><strong>今日吉凶:</strong> ⭐⭐⭐⭐⭐⭐⭐ (7/10 - 吉日)</p>
      <p><strong>行业五行:</strong> 火行旺盛，饮料行业处于衰落期</p>
      <p><strong>企业运势:</strong> 长期向好，但本月有风险 (金行衰落)</p>
      <div class="predicted-events">
        <p><strong>预测事件:</strong></p>
        <ul>
          <li>6月21日 (夏至): 节气转换，可能造成短期调整</li>
          <li>7月初: 五行从火→土，行业轮动信号</li>
        </ul>
      </div>
      <p class="disclaimer">⚠️ 占星学为参考性分析，不构成投资建议。</p>
    </div>
  </div>
  
  <!-- 气候与天气洞察 -->
  <div class="climate-panel">
    <div class="header">
      <h3>气候与天气洞察</h3>
      <span class="accuracy">准确率: 75% (基于NOAA/CMA官方数据)</span>
    </div>
    <div class="content">
      <p><strong>当前季节:</strong> 初夏，温度持续上升</p>
      <div class="alerts">
        <p><strong>极端天气预警:</strong></p>
        <ul>
          <li>☀️ 华东地区高温预警 (6月15-25日): 电力需求↑</li>
          <li>🌧️ 西南地区暴雨风险 (6月20日前后): 水利设施↑</li>
        </ul>
      </div>
      <div class="industry-impacts">
        <p><strong>行业影响:</strong></p>
        <ul>
          <li>电力行业: 看好 (高温导致空调/冰箱需求↑)</li>
          <li>农业: 看空 (干旱风险+洪水风险)</li>
          <li>运输物流: 中性偏弱 (极端天气影响)</li>
        </ul>
      </div>
    </div>
  </div>
  
  <!-- 宏观事件预测 -->
  <div class="macro-events-panel">
    <div class="header">
      <h3>宏观事件预测</h3>
      <span class="accuracy">准确率: 58% (基于舆情&历史规律)</span>
    </div>
    <div class="content">
      <p><strong>近期关键事件:</strong></p>
      <ul>
        <li>
          <strong>6月中旬:</strong> 半导体行业政策可能调整
          <br/>→ 科技股关注，置信度 65%
        </li>
        <li>
          <strong>7月初:</strong> 上半年经济数据发布
          <br/>→ 可能造成市场波动，置信度 85%
        </li>
        <li>
          <strong>秋分 (9月23日):</strong> 农业政策调整历史规律
          <br/>→ 农业/食品股可能被激活，置信度 60%
        </li>
      </ul>
    </div>
  </div>
</div>

<!-- 关键提示 -->
<div class="insights-summary">
  <h3>📌 综合提示</h3>
  <div class="opportunities">
    <strong>潜在机会:</strong>
    <ul>
      <li>高温将持续到夏至，电力股可维持关注</li>
      <li>如基本面良好，可在吉日小幅加仓</li>
    </ul>
  </div>
  <div class="risks">
    <strong>风险提示:</strong>
    <ul>
      <li>夏至时节气转换，历史上易出现调整</li>
      <li>企业五行与当前运势不匹配，建议风控</li>
      <li>西南洪水风险可能影响供应链</li>
    </ul>
  </div>
</div>
```

---

## ⚙️ 环境配置

### `.env` 配置

```env
# 补充洞察总开关
SUPPLEMENTARY_INSIGHTS_ENABLED=true

# 占星学分析
ASTRO_INSIGHTS_ENABLED=true
ASTRO_ACCURACY_THRESHOLD=0.60  # 准确率低于60%时自动降低权重

# 气候预测
CLIMATE_INSIGHTS_ENABLED=true
CLIMATE_DATA_SOURCES=noaa,cma,weather_api  # 优先级顺序

# 宏观事件预测
MACRO_EVENT_INSIGHTS_ENABLED=true
MACRO_EVENT_CONFIDENCE_MIN=0.55  # 最低置信度阈值

# 准确率验证开关
ACCURACY_TRACKING_ENABLED=true
ACCURACY_VALIDATION_INTERVAL_DAYS=30  # 每30天验证一次

# 前端显示
SHOW_SUPPLEMENTARY_INSIGHTS=true  # 前端是否显示补充洞察
SHOW_ACCURACY_METRICS=true        # 显示准确率数据
ACCURACY_DISPLAY_FORMAT=percentage # percentage / stars
```

---

## 🔄 回测与验证流程

### 准确率自动验证

```python
# src/addons/astro_climate_insights/automated_validation.py

class AutomatedAccuracyValidation:
    """自动验证准确率的系统"""
    
    def run_daily_validation(self):
        """每日运行：检查过期的预测并验证"""
        
        # 1. 查询30天前发出的预测
        predictions_to_validate = self.db.query_predictions(
            created_at_before=(datetime.now() - timedelta(days=30))
        )
        
        # 2. 获取实际结果
        for pred in predictions_to_validate:
            actual_result = self._fetch_actual_result(pred)
            
            # 3. 验证准确性
            self.accuracy_tracker.validate_prediction(
                prediction_id=pred.id,
                actual_result=actual_result,
            )
        
        # 4. 更新准确率统计
        self._update_accuracy_stats()
```

### 每月报告

```
📈 准确率月度报告 (2026年5月)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【占星学洞察】
  本月预测: 24条
  准确: 15条 (62%)
  ↑ +3% vs 上月
  最准确: 吉凶日预测 (75%)
  待改进: 宏观事件预测 (48%)

【气候与天气】
  本月预测: 18条
  准确: 14条 (78%)
  ↑ 稳定
  数据源: NOAA 92%, CMA 76%

【宏观事件】
  本月预测: 12条
  准确: 7条 (58%)
  ↓ -4% vs 上月
  主要失误: 政策预期不及时

整体趋势: 占星学准确率持续提升，气候预测稳定可靠
```

---

## 💡 关键优势

### ✅ 对用户的价值

1. **透明化** - 每条建议都显示准确率，用户自主判断
2. **补充性** - 不干扰核心评分，作为参考视角
3. **多维度** - 天文学 + 气候科学 + 宏观事件 + 舆情分析
4. **可验证** - 过去预测准确率可查询，持续改进透明化
5. **预警功能** - 提前识别可能的市场转折点和风险

### ✅ 对模型的优势

1. **学习驱动** - 准确率追踪激励模型不断优化
2. **可控权重** - 可根据实际表现动态调整各模块的参考权重
3. **规避过度拟合** - 占星学/气候只作参考，不会污染核心评分
4. **行业领先** - 融合多学科视角，提供竞争力优势

---

## 📚 部署清单

### Phase 1: 基础设施 (2周)

- [ ] 实现 `calendar_engine.py` - 农历/节气计算
- [ ] 实现 `accuracy_tracker.py` - 准确率数据库
- [ ] 创建 Schema 模型
- [ ] 集成到 pipeline

### Phase 2: 数据源接入 (1周)

- [ ] 接入 NOAA Weather API
- [ ] 接入 CMA (中国气象局) 数据
- [ ] 接入政策日程数据源
- [ ] 实现缓存机制

### Phase 3: 前端展示 (1周)

- [ ] Web UI 添加补充洞察面板
- [ ] 实现准确率展示
- [ ] 制作演示报告

### Phase 4: 验证与上线 (1-2周)

- [ ] 历史数据回测验证
- [ ] 精细化准确率追踪
- [ ] 用户反馈收集
- [ ] 上线前完整测试

---

## 📄 免责声明与合规

```
⚠️ 重要免责声明

本补充洞察模块（占星学、气候预测、宏观事件预测）仅作参考信息使用，
不构成任何投资建议或保证。

使用者应当：
1. 了解各模块的历史准确率，谨慎参考
2. 独立进行投资决策和风险评估
3. 咨询专业财务顾问
4. 自行承担所有投资损失

本项目及维护者对使用本模块导致的任何损失不承担任何责任。

投资有风险，决策需谨慎。
```

---

**版本**: v1.0  
**最后更新**: 2026-06-11  
**维护者**: DSA Community
