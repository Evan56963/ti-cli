from dataclasses import dataclass
from enum import Enum, StrEnum, unique
from dearpygui import dearpygui as dpg

@unique
class Tag(StrEnum):
    SYMBOLS_INPUT = "symbols_input"
    MARKET_RADIO = "market_radio"
    INTERVAL_RADIO = "interval_radio"
    START_DATE = "start_date"
    END_DATE = "end_date"
    OUTPUT_TEXT = "output_text"
    MAIN_WINDOW = "main_window"

@dataclass
class Option:
    label: str
    value: str
    
@unique
class Market(Enum):
    TAIWAN_STOCK = Option(label="Taiwan Stock (tw)", value="tw")
    OTC = Option(label="OTC (two)", value="two")
    US_STOCK = Option(label="US Stock (us)", value="us")
    ETF = Option(label="ETF", value="etf")
    INDEX = Option(label="Index", value="index")
    CRYPTO = Option(label="Crypto", value="crypto")
    FOREX = Option(label="Forex", value="forex")
    FUTURES = Option(label="Futures", value="futures")
    
@unique
class Interval(Enum):
    ONE_MINUTE = Option(label="1 Minute (1m)", value="1m")
    FIVE_MINUTES = Option(label="5 Minutes (5m)", value="5m")
    FIFTEEN_MINUTES = Option(label="15 Minutes (15m)", value="15m")
    THIRTY_MINUTES = Option(label="30 Minutes (30m)", value="30m")
    ONE_HOUR = Option(label="1 Hour (1h)", value="1h")
    ONE_DAY = Option(label="1 Day (1d)", value="1d")
    ONE_WEEK = Option(label="1 Week (1wk)", value="1wk")
    ONE_MONTH = Option(label="1 Month (1mo)", value="1mo")


class InputComponents:
    """Input components"""
    
    def get_symbols(self) -> list[str]:
        """Get stock symbol list"""
        symbols_text = dpg.get_value(Tag.SYMBOLS_INPUT)
        return [s.strip() for s in symbols_text.split() if s.strip()]
    
    def get_market(self) -> str | None:
        """Get selected market"""
        market_selection = dpg.get_value(Tag.MARKET_RADIO)
        return next((m.value.value for m in Market if m.value.label == market_selection), None)
    
    def get_interval(self) -> str | None:
        """Get selected time interval"""
        interval_selection = dpg.get_value(Tag.INTERVAL_RADIO)
        return next((i.value.value for i in Interval if i.value.label == interval_selection), None)
    
    def get_date_range(self) -> tuple[str, str]:
        """Get date range"""
        start_date = dpg.get_value(Tag.START_DATE)
        end_date = dpg.get_value(Tag.END_DATE)
        return start_date, end_date


class OutputComponents:
    """Output components"""
    
    def clear(self):
        """Clear output text"""
        dpg.set_value(Tag.OUTPUT_TEXT, "")
    
    def append(self, text: str):
        """Append output text"""
        current = dpg.get_value(Tag.OUTPUT_TEXT)
        dpg.set_value(Tag.OUTPUT_TEXT, f"{current}{text}\n")