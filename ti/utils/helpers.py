SUFFIX_MAP = {
    "tw": ".TW",
    "two": ".TWO",
    "us": "",
    "etf": "",
    "index": "",
    "crypto": "-USD",
    "forex": "=X",
    "futures": ""
}

PERIOD_MAP = {
    "1m": "7d",
    "5m": "7d",
    "15m": "7d",
    "30m": "7d",
    "1h": "1mo",
    "1d": "1y",
    "1wk": "2y",
    "1mo": "5y",
}
    

def get_ticker_with_suffix(ticker: str, market: str) -> str:
        """Format symbol based on market"""
        suffix = SUFFIX_MAP.get(market, "")
        if suffix and not ticker.endswith(suffix):
            return ticker + suffix
        return ticker

def get_period_by_interval(interval: str) -> str:
        """Get period based on time interval setting"""
        return PERIOD_MAP.get(interval, '1y')