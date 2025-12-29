"""
More data sources can be added in the future.
"""
import yfinance as yf

class YahooFinanceFetcher:
    """Yahoo Finance data fetcher"""
    
    @staticmethod
    def get_stock_data(symbol, period, interval):
        """Fetch data"""
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, interval=interval)
        
        return data[['Open', 'High', 'Low', 'Close', 'Volume']]
    
    @staticmethod
    def get_stock_data_range(symbol, start_date, end_date, interval):
        """Fetch data based on date range"""
        ticker = yf.Ticker(symbol)
        data = ticker.history(start=start_date, end=end_date, interval=interval)
        
        return data[['Open', 'High', 'Low', 'Close', 'Volume']]