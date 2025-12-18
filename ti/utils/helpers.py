class SUFFIX_MAP:
    tw = ".TW",
    two = ".TWO"
    us = ""
    etf = ""
    index = ""
    crypto = "-USD"
    forex = "=X"
    futures = ""

class PERIOD_MAP:
    m1 = "7d"
    m5 = "7d"
    m15 = "7d"
    m30 = "7d"
    h1 = "1mo"
    d1 = "1y"
    wk1 = "2y"
    mo1 = "5y"
    

def get_ticker_with_suffix(ticker: str, market: str) -> str:
        """根據市場格式化股票代號"""
        suffix = getattr(SUFFIX_MAP, market, '')
        if suffix and not ticker.endswith(suffix):
            return ticker + suffix
        return ticker

def get_period_by_interval(interval: str) -> str:
        """根據時間間隔設定獲取期間"""
        return getattr(PERIOD_MAP, interval, '1y')