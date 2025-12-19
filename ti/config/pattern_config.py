from typing import Optional
from enum import StrEnum, unique
from dataclasses import dataclass

@unique
class PatternType(StrEnum):
    REVERSAL = "反轉型態"
    CONTINUATION = "持續型態"
    NEUTRAL = "中性型態"
    
@dataclass
class CandlePattern():
    ta_function: str
    chinese_name: str
    pattern_type: PatternType
    needs_penetration: bool = False
    has_direction: bool = False
    bullish_name: Optional[str] = None
    bearish_name: Optional[str] = None
    description: Optional[str] = None

# K線型態函數與中文註解對應表
CANDLE_PATTERNS: dict[str, CandlePattern] = {
    # 反轉型態
    'CDLHAMMER': CandlePattern(
        ta_function='CDLHAMMER', chinese_name='錘頭', pattern_type=PatternType.REVERSAL,
        description="底部反轉訊號，長下影線，小實體"
    ),
    'CDLHANGINGMAN': CandlePattern(
        ta_function='CDLHANGINGMAN', chinese_name='上吊線', pattern_type=PatternType.REVERSAL,
        description="頂部反轉訊號，長下影線，小實體"
    ),
    'CDLINVERTEDHAMMER': CandlePattern(
        ta_function='CDLINVERTEDHAMMER', chinese_name='倒錘頭', pattern_type=PatternType.REVERSAL,
        description="底部反轉訊號，長上影線，小實體"
    ),
    'CDLSHOOTINGSTAR': CandlePattern(
        ta_function='CDLSHOOTINGSTAR', chinese_name='射擊星', pattern_type=PatternType.REVERSAL,
        description="頂部反轉訊號，長上影線，小實體"
    ),
    
    # 吞沒型態
    'CDLENGULFING': CandlePattern(
        ta_function='CDLENGULFING', chinese_name='吞沒形態', pattern_type=PatternType.REVERSAL,
        has_direction=True, bullish_name='多頭吞沒', bearish_name='空頭吞沒',
        description="第二根K線完全包含第一根K線"
    ),
    
    # 晨星/暮星系列
    'CDLMORNINGSTAR': CandlePattern(
        ta_function='CDLMORNINGSTAR', chinese_name='晨星', pattern_type=PatternType.REVERSAL,
        needs_penetration=True, description="三K線底部反轉型態"
    ),
    'CDLEVENINGSTAR': CandlePattern(
        ta_function='CDLEVENINGSTAR', chinese_name='暮星', pattern_type=PatternType.REVERSAL,
        needs_penetration=True, description="三K線頂部反轉型態"
    ),
    'CDLMORNINGDOJISTAR': CandlePattern(
        ta_function='CDLMORNINGDOJISTAR', chinese_name='十字晨星', pattern_type=PatternType.REVERSAL,
        needs_penetration=True, description="中間為十字線的晨星型態"
    ),
    'CDLEVENINGDOJISTAR': CandlePattern(
        ta_function='CDLEVENINGDOJISTAR', chinese_name='十字暮星', pattern_type=PatternType.REVERSAL,
        needs_penetration=True, description="中間為十字線的暮星型態"
    ),
    
    # 十字線系列
    'CDLDOJI': CandlePattern(
        ta_function='CDLDOJI', chinese_name='十字', pattern_type=PatternType.NEUTRAL,
        description="開盤價等於收盤價，市場猶豫"
    ),
    'CDLDOJISTAR': CandlePattern(
        ta_function='CDLDOJISTAR', chinese_name='十字星', pattern_type=PatternType.REVERSAL,
        description="跳空的十字線"
    ),
    'CDLDRAGONFLYDOJI': CandlePattern(
        ta_function='CDLDRAGONFLYDOJI', chinese_name='蜻蜓十字', pattern_type=PatternType.REVERSAL,
        description="只有下影線的十字線"
    ),
    'CDLGRAVESTONEDOJI': CandlePattern(
        ta_function='CDLGRAVESTONEDOJI', chinese_name='墓碑十字', pattern_type=PatternType.REVERSAL,
        description="只有上影線的十字線"
    ),
    'CDLLONGLEGGEDDOJI': CandlePattern(
        ta_function='CDLLONGLEGGEDDOJI', chinese_name='長腿十字', pattern_type=PatternType.NEUTRAL,
        description="上下都有長影線的十字線"
    ),
    
    # 三兵系列
    'CDL3WHITESOLDIERS': CandlePattern(
        ta_function='CDL3WHITESOLDIERS', chinese_name='三白兵', pattern_type=PatternType.CONTINUATION,
        description="三根連續上漲的陽線"
    ),
    'CDL3BLACKCROWS': CandlePattern(
        ta_function='CDL3BLACKCROWS', chinese_name='三隻烏鴉', pattern_type=PatternType.CONTINUATION,
        description="三根連續下跌的陰線"
    ),
    'CDLIDENTICAL3CROWS': CandlePattern(
        ta_function='CDLIDENTICAL3CROWS', chinese_name='三胞胎烏鴉', pattern_type=PatternType.CONTINUATION,
        description="三根相似的連續下跌陰線"
    ),
    'CDL2CROWS': CandlePattern(
        ta_function='CDL2CROWS', chinese_name='兩隻烏鴉', pattern_type=PatternType.REVERSAL,
        description="兩根下跌陰線，頂部反轉訊號"
    ),
    
    # 內外包型態
    'CDL3INSIDE': CandlePattern(
        ta_function='CDL3INSIDE', chinese_name='三內部漲跌', pattern_type=PatternType.REVERSAL,
        has_direction=True, bullish_name='三內部上漲', bearish_name='三內部下跌',
        description="三K線內包型態"
    ),
    'CDL3OUTSIDE': CandlePattern(
        ta_function='CDL3OUTSIDE', chinese_name='三外部漲跌', pattern_type=PatternType.REVERSAL,
        has_direction=True, bullish_name='三外部上漲', bearish_name='三外部下跌',
        description="三K線外包型態"
    ),
    
    # 孕線系列
    'CDLHARAMI': CandlePattern(
        ta_function='CDLHARAMI', chinese_name='孕線', pattern_type=PatternType.REVERSAL,
        description="第二根K線被第一根完全包含"
    ),
    'CDLHARAMICROSS': CandlePattern(
        ta_function='CDLHARAMICROSS', chinese_name='十字孕線', pattern_type=PatternType.REVERSAL,
        description="第二根為十字線的孕線型態"
    ),
    
    # 光頭光腳系列
    'CDLMARUBOZU': CandlePattern(
        ta_function='CDLMARUBOZU', chinese_name='光頭光腳', pattern_type=PatternType.CONTINUATION,
        has_direction=True, bullish_name='上漲光頭光腳', bearish_name='下跌光頭光腳',
        description="沒有上下影線的K線"
    ),
    'CDLCLOSINGMARUBOZU': CandlePattern(
        ta_function='CDLCLOSINGMARUBOZU', chinese_name='光頭光腳(單頭腳判定)', pattern_type=PatternType.CONTINUATION,
        has_direction=True, bullish_name='光頭', bearish_name='光腳',
        description="只有一端沒有影線"
    ),
    
    # 打擊系列
    'CDL3LINESTRIKE': CandlePattern(
        ta_function='CDL3LINESTRIKE', chinese_name='三線打擊', pattern_type=PatternType.REVERSAL,
        has_direction=True, bullish_name='三線打擊上漲', bearish_name='三線打擊下跌',
        description="三根同向K線後的反轉型態"
    ),
    'CDLCOUNTERATTACK': CandlePattern(
        ta_function='CDLCOUNTERATTACK', chinese_name='反擊線', pattern_type=PatternType.REVERSAL,
        description="收盤價相同的反向K線組合"
    ),
    
    # 三法系列
    'CDLRISEFALL3METHODS': CandlePattern(
        ta_function='CDLRISEFALL3METHODS', chinese_name='上升/下降三法', pattern_type=PatternType.CONTINUATION,
        has_direction=True, bullish_name='上升三法', bearish_name='下降三法',
        description="趨勢中的整理型態"
    ),
    'CDLXSIDEGAP3METHODS': CandlePattern(
        ta_function='CDLXSIDEGAP3METHODS', chinese_name='跳空三法', pattern_type=PatternType.CONTINUATION,
        has_direction=True, bullish_name='上升跳空三法', bearish_name='下降跳空三法',
        description="跳空後的整理型態"
    ),
    
    # 穿透型態
    'CDLPIERCING': CandlePattern(
        ta_function='CDLPIERCING', chinese_name='刺穿形態', pattern_type=PatternType.REVERSAL,
        description="陽線向上穿透前一根陰線的一半以上"
    ),
    'CDLDARKCLOUDCOVER': CandlePattern(
        ta_function='CDLDARKCLOUDCOVER', chinese_name='烏雲蓋頂', pattern_type=PatternType.REVERSAL,
        needs_penetration=True, description="陰線向下穿透前一根陽線的一半以上"
    ),
    
    # 缺口型態
    'CDLGAPSIDESIDEWHITE': CandlePattern(
        ta_function='CDLGAPSIDESIDEWHITE', chinese_name='缺口上漲', pattern_type=PatternType.CONTINUATION,
        description="向上跳空的兩根陽線"
    ),
    'CDLUPSIDEGAP2CROWS': CandlePattern(
        ta_function='CDLUPSIDEGAP2CROWS', chinese_name='向上跳空兩隻烏鴉', pattern_type=PatternType.REVERSAL,
        description="向上跳空後的兩根陰線"
    ),
    'CDLTASUKIGAP': CandlePattern(
        ta_function='CDLTASUKIGAP', chinese_name='跳空並列(月缺)', pattern_type=PatternType.CONTINUATION,
        description="跳空後的並列K線"
    ),
    
    # 特殊型態
    'CDLABANDONEDBABY': CandlePattern(
        ta_function='CDLABANDONEDBABY', chinese_name='棄嬰', pattern_type=PatternType.REVERSAL,
        has_direction=True, bullish_name='棄嬰上漲', bearish_name='棄嬰下跌',
        description="中間跳空的三K線反轉型態"
    ),
    'CDLBELTHOLD': CandlePattern(
        ta_function='CDLBELTHOLD', chinese_name='捉腰帶線', pattern_type=PatternType.REVERSAL,
        description="長實體，一端沒有影線"
    ),
    'CDLBREAKAWAY': CandlePattern(
        ta_function='CDLBREAKAWAY', chinese_name='脫離', pattern_type=PatternType.REVERSAL,
        description="五K線的突破型態"
    ),
    'CDLKICKING': CandlePattern(
        ta_function='CDLKICKING', chinese_name='反沖形態', pattern_type=PatternType.REVERSAL,
        description="兩根跳空的光頭光腳K線"
    ),
    'CDLKICKINGBYLENGTH': CandlePattern(
        ta_function='CDLKICKINGBYLENGTH', chinese_name='反沖-長短判斷', pattern_type=PatternType.REVERSAL,
        description="根據K線長度判斷的反沖型態"
    ),
    
    # 其他型態
    'CDLADVANCEBLOCK': CandlePattern(
        ta_function='CDLADVANCEBLOCK', chinese_name='大敵當前', pattern_type=PatternType.REVERSAL,
        description="三根逐漸縮小的陽線"
    ),
    'CDLCONCEALBABYSWALL': CandlePattern(
        ta_function='CDLCONCEALBABYSWALL', chinese_name='藏嬰吞沒', pattern_type=PatternType.REVERSAL,
        description="特殊的吞沒型態"
    ),
    'CDL3STARSINSOUTH': CandlePattern(
        ta_function='CDL3STARSINSOUTH', chinese_name='南方三星', pattern_type=PatternType.REVERSAL,
        description="三K線的底部反轉型態"
    ),
    'CDLHIKKAKE': CandlePattern(
        ta_function='CDLHIKKAKE', chinese_name='Hikkake 陷阱', pattern_type=PatternType.REVERSAL,
        description="日本的陷阱型態"
    ),
    'CDLHIKKAKEMOD': CandlePattern(
        ta_function='CDLHIKKAKEMOD', chinese_name='Hikkake Modified', pattern_type=PatternType.REVERSAL,
        description="修正版的Hikkake型態"
    ),
    'CDLHOMINGPIGEON': CandlePattern(
        ta_function='CDLHOMINGPIGEON', chinese_name='家鴿', pattern_type=PatternType.REVERSAL,
        description="特殊的孕線變化型態"
    ),
    'CDLINNECK': CandlePattern(
        ta_function='CDLINNECK', chinese_name='頸內線', pattern_type=PatternType.CONTINUATION,
        description="頸線內的持續型態"
    ),
    'CDLONNECK': CandlePattern(
        ta_function='CDLONNECK', chinese_name='頸上線', pattern_type=PatternType.CONTINUATION,
        description="頸線上的持續型態"
    ),
    'CDLLADDERBOTTOM': CandlePattern(
        ta_function='CDLLADDERBOTTOM', chinese_name='梯形底部', pattern_type=PatternType.REVERSAL,
        description="階梯式的底部型態"
    ),
    'CDLMATCHINGLOW': CandlePattern(
        ta_function='CDLMATCHINGLOW', chinese_name='匹配低點', pattern_type=PatternType.REVERSAL,
        description="相同低點的K線組合"
    ),
    'CDLMATHOLD': CandlePattern(
        ta_function='CDLMATHOLD', chinese_name='鋪墊', pattern_type=PatternType.CONTINUATION,
        needs_penetration=True, description="趨勢中的整理型態"
    ),
    'CDLRICKSHAWMAN': CandlePattern(
        ta_function='CDLRICKSHAWMAN', chinese_name='黃包車夫', pattern_type=PatternType.NEUTRAL,
        description="長上下影線的小實體K線"
    ),
    'CDLSEPARATINGLINES': CandlePattern(
        ta_function='CDLSEPARATINGLINES', chinese_name='分離線', pattern_type=PatternType.CONTINUATION,
        description="相同開盤價的反向K線"
    ),
    'CDLSTALLEDPATTERN': CandlePattern(
        ta_function='CDLSTALLEDPATTERN', chinese_name='停滯形態', pattern_type=PatternType.REVERSAL,
        description="上升趨勢中的停滯訊號"
    ),
    'CDLSTICKSANDWICH': CandlePattern(
        ta_function='CDLSTICKSANDWICH', chinese_name='三明治', pattern_type=PatternType.REVERSAL,
        description="三K線的夾心型態"
    ),
    'CDLTAKURI': CandlePattern(
        ta_function='CDLTAKURI', chinese_name='探水竿', pattern_type=PatternType.REVERSAL,
        description="長下影線的底部反轉訊號"
    ),
    'CDLTHRUSTING': CandlePattern(
        ta_function='CDLTHRUSTING', chinese_name='向上突破', pattern_type=PatternType.CONTINUATION,
        description="向上突破的持續型態"
    ),
    'CDLTRISTAR': CandlePattern(
        ta_function='CDLTRISTAR', chinese_name='三星', pattern_type=PatternType.REVERSAL,
        description="三根十字線組成的反轉型態"
    ),
    'CDLUNIQUE3RIVER': CandlePattern(
        ta_function='CDLUNIQUE3RIVER', chinese_name='奇特三河床', pattern_type=PatternType.REVERSAL,
        description="特殊的三K線底部型態"
    ),
    'CDLHIGHWAVE': CandlePattern(
        ta_function='CDLHIGHWAVE', chinese_name='風高浪大線', pattern_type=PatternType.NEUTRAL,
        description="長上下影線，市場不確定"
    ),
    'CDLLONGLINE': CandlePattern(
        ta_function='CDLLONGLINE', chinese_name='長蠟燭', pattern_type=PatternType.CONTINUATION,
        description="長實體的K線"
    ),
    'CDLSHORTLINE': CandlePattern(
        ta_function='CDLSHORTLINE', chinese_name='短蠟燭', pattern_type=PatternType.NEUTRAL,
        description="短實體的K線"
    ),
    'CDLSPINNINGTOP': CandlePattern(
        ta_function='CDLSPINNINGTOP', chinese_name='紡錘線', pattern_type=PatternType.NEUTRAL,
        description="小實體，長上下影線"
    ),
}