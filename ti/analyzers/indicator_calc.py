import talib
import pandas as pd

class TechnicalIndicatorCalculator:
    """Technical indicator calculator - Responsible for calculating various technical indicators"""

    @staticmethod
    def calculate_all_indicators(data:pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators"""
        
        high = data['High'].values
        low = data['Low'].values
        close = data['Close'].values
        
        indicators = pd.DataFrame(index=data.index)
        
        
        # RSI indicator group
        indicators['RSI_5'] = talib.RSI(close, timeperiod=5)
        indicators['RSI_7'] = talib.RSI(close, timeperiod=7)
        indicators['RSI_10'] = talib.RSI(close, timeperiod=10)
        indicators['RSI_14'] = talib.RSI(close, timeperiod=14)
        indicators['RSI_21'] = talib.RSI(close, timeperiod=21)
                
        # MACD indicator group
        macd, macd_signal, macd_hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        indicators['DIF'] = macd
        indicators['MACD'] = macd_signal
        indicators['MACD_Histogram'] = macd_hist
                
        # KDJ indicator group
        slowk, slowd = talib.STOCH(high, low, close, fastk_period=9, slowk_period=3, slowd_period=3)
        fastk, fastd = talib.STOCHF(high, low, close, fastk_period=9, fastd_period=1, fastd_matype=0)
        indicators['RSV'] = fastk    
        indicators['K_Value'] = slowk
        indicators['D_Value'] = slowd
        indicators['J_Value'] = 3 * slowk - 2 * slowd

        # MA moving average group
        indicators['MA5'] = talib.SMA(close, timeperiod=5)
        indicators['MA10'] = talib.SMA(close, timeperiod=10)
        indicators['MA20'] = talib.SMA(close, timeperiod=20)
        indicators['MA60'] = talib.SMA(close, timeperiod=60)
                
        # EMA exponential moving average group
        indicators['EMA12'] = talib.EMA(close, timeperiod=12)
        indicators['EMA26'] = talib.EMA(close, timeperiod=26)
                
        # Bollinger Bands group
        upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        indicators['Bollinger_Upper'] = upper
        indicators['Bollinger_Middle'] = middle
        indicators['Bollinger_Lower'] = lower
                
        # Other technical indicators
        indicators['ATR'] = talib.ATR(high, low, close, timeperiod=14)
        indicators['CCI'] = talib.CCI(high, low, close, timeperiod=14)
        indicators['Williams_R'] = talib.WILLR(high, low, close, timeperiod=14)
        indicators['Momentum'] = talib.MOM(close, timeperiod=10)
        
        return indicators