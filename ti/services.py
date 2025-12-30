from ti.providers import YahooFinanceFetcher
from ti.analyzers.indicator_calc import TechnicalIndicatorCalculator
from ti.analyzers.candle_pattern import CandlePatternDetector
from ti.database.repositories import MarketDataRepository
from ti.utils.helpers import get_ticker_with_suffix, get_period_by_interval
import pandas as pd

class MarketService:
    """
    Responsible for integrating data fetching, technical indicator calculation
    , and candlestick pattern detection
    """

    def __init__(self):
        self.detector = CandlePatternDetector()
    
    def fetch_and_store(self, symbol: str, market: str, interval: str, mode: str) -> dict[str, int | str]:
        """Fetch and store data and technical indicators"""
        # Format symbol
        formatted_symbol = get_ticker_with_suffix(symbol, market)
        period = get_period_by_interval(interval)

        # Fetch data
        stock_data = YahooFinanceFetcher.get_stock_data(formatted_symbol, period, interval)
        
        # Calculate technical indicators
        indicators = TechnicalIndicatorCalculator.calculate_all_indicators(stock_data)
        
        # Detect candlestick patterns
        pattern_features = self.detector.detect_and_combine(stock_data)
        
        # Combine all data
        combined_data = pd.concat([stock_data, indicators, pattern_features], axis=1)
        
        if mode=='save':
            # Save data to database
            repo = MarketDataRepository(market)
            saved_count = repo.save_market_data(combined_data, symbol, interval)
        else:
            saved_count = 0
        
        return {
            'symbol': symbol,
            'market': market,
            'interval': interval,
            'data_count': len(stock_data),
            'indicator_count': len(indicators.columns),
            'pattern_count': (pattern_features != '').sum(),
            'saved_count': saved_count,
            'combined_data': combined_data
        }
    
    def fetch_and_store_range(self, symbol: str, market: str, interval: str, start_date: str, end_date: str, mode: str) -> dict[str, int | str]:  
        """Fetch and store data and technical indicators based on date range"""

        # Format symbol
        formatted_symbol = get_ticker_with_suffix(symbol, market)

        # Fetch data
        stock_data = YahooFinanceFetcher.get_stock_data_range(formatted_symbol, start_date, end_date, interval)
        
        # Calculate technical indicators
        indicators = TechnicalIndicatorCalculator.calculate_all_indicators(stock_data)
        
        # Detect candlestick patterns
        pattern_features = self.detector.detect_and_combine(stock_data)
            
        # Combine all data
        combined_data = pd.concat([stock_data, indicators, pattern_features], axis=1)
        
        if mode=='save':
            # Save data to database
            repo = MarketDataRepository(market)
            saved_count = repo.save_market_data(combined_data, symbol, interval)
        else:
            saved_count = 0
        
        return {
            'symbol': symbol,
            'market': market,
            'interval': interval,
            'data_count': len(stock_data),
            'indicator_count': len(indicators.columns),
            'pattern_count': (pattern_features != '').sum(),
            'saved_count': saved_count,
            'combined_data': combined_data
        }

class SignalService:
    """Trading signal service"""