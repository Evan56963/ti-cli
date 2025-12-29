from sqlmodel import SQLModel, Field, inspect
from datetime import datetime
from typing import Optional
from ti.database.connection import get_connection

class MarketDataBaseModel(SQLModel):
    """Data base model"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(max_length=20, index=True)
    interval: str = Field(max_length=10, index=True)
    timestamp: datetime = Field(index=True)
    
    # OHLCV data
    open: Optional[float] = Field(default=None, sa_column_kwargs={"name": "open"})
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = Field(default=None, sa_column_kwargs={"name": "close"})
    volume: Optional[int] = None
    
    # RSI indicators
    rsi_5: Optional[float] = None
    rsi_7: Optional[float] = None
    rsi_10: Optional[float] = None
    rsi_14: Optional[float] = None
    rsi_21: Optional[float] = None
    
    # MACD indicators
    dif: Optional[float] = None
    macd: Optional[float] = None
    macd_histogram: Optional[float] = None
    
    # KDJ indicators
    rsv: Optional[float] = None
    k_value: Optional[float] = None
    d_value: Optional[float] = None
    j_value: Optional[float] = None
    
    # MA indicators
    ma5: Optional[float] = None
    ma10: Optional[float] = None
    ma20: Optional[float] = None
    ma60: Optional[float] = None
    
    # EMA indicators
    ema12: Optional[float] = None
    ema26: Optional[float] = None
    
    # Bollinger Bands
    bollinger_upper: Optional[float] = None
    bollinger_middle: Optional[float] = None
    bollinger_lower: Optional[float] = None
    
    # Other indicators
    atr: Optional[float] = None
    cci: Optional[float] = None
    williams_r: Optional[float] = None
    momentum: Optional[float] = None
    
    # Pattern features
    pattern_feature: Optional[str] = Field(default=None, max_length=500)
    
    # Last update time
    last_update: Optional[datetime] = None


class StockDataTW(MarketDataBaseModel, table=True):
    """Taiwan stock market data table"""
    __tablename__ = "stock_data_tw"

class StockDataUS(MarketDataBaseModel, table=True):
    """US stock market data table"""
    __tablename__ = "stock_data_us"

class Crypto(MarketDataBaseModel, table=True):
    """Cryptocurrency data table"""
    
class Index(MarketDataBaseModel, table=True):
    """Index data table"""
    
class ETF(MarketDataBaseModel, table=True):
    """ETF data table"""
    
class Forex(MarketDataBaseModel, table=True):
    """Forex data table"""

class Futures(MarketDataBaseModel, table=True):
    """Futures data table"""


MARKET_MODELS: dict[str, type[MarketDataBaseModel]] = {
    "tw": StockDataTW,
    "two": StockDataTW,
    "us": StockDataUS,
    "crypto": Crypto,
    "index": Index,
    "etf": ETF,
    "forex": Forex,
    "futures": Futures,
}

engine = get_connection()
inspector = inspect(engine)

def get_model_count() -> int:
    """Return the count of market models"""
    return len(MARKET_MODELS)

def get_model_by_market(market: str) -> type[MarketDataBaseModel]:
    """Get the corresponding model based on market code"""
    model = MARKET_MODELS.get(market.lower())
    if not model:
        raise ValueError(f"Unsupported market: {market}. Supported markets: {', '.join(MARKET_MODELS.keys())}")
    return model

def create_tables():
    """Create all tables"""
    SQLModel.metadata.create_all(engine)

def create_table_by_market(market: str):
    """Create specified table based on market"""
    model = get_model_by_market(market)
    model.metadata.create_all(engine)

def drop_tables():
    """Drop all tables"""
    SQLModel.metadata.drop_all(engine)

def drop_table_by_market(market: str):
    """Drop specified table based on market"""
    model = get_model_by_market(market)
    model.metadata.drop_all(engine)

def list_all_tables() -> list[str]:
    """List all tables in the database"""
    return inspector.get_table_names()