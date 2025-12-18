from enum import Enum
from dataclasses import dataclass
from dearpygui import dearpygui as dpg
from ti.services import StockDataService
from ti.database import tables

@dataclass
class Option:
    label: str
    value: str

class Market(Enum):
    TAIWAN_STOCK = Option("Taiwan Stock (tw)", "tw")
    OTC = Option("OTC (two)", "two")
    US_STOCK = Option("US Stock (us)", "us")
    ETF = Option("ETF", "etf")
    INDEX = Option("Index", "index")
    CRYPTO = Option("Crypto", "crypto")
    FOREX = Option("Forex", "forex")
    FUTURES = Option("Futures", "futures")

class Interval(Enum):
    ONE_MINUTE = Option("1 Minute (1m)", "1m")
    FIVE_MINUTES = Option("5 Minutes (5m)", "5m")
    FIFTEEN_MINUTES = Option("15 Minutes (15m)", "15m")
    THIRTY_MINUTES = Option("30 Minutes (30m)", "30m")
    ONE_HOUR = Option("1 Hour (1h)", "1h")
    ONE_DAY = Option("1 Day (1d)", "1d")
    ONE_WEEK = Option("1 Week (1wk)", "1wk")
    ONE_MONTH = Option("1 Month (1mo)", "1mo")

service = StockDataService()

class Gui:
    """技術指標分析工具圖形介面"""

    def __init__(self):
        self.controller = Controller()
    
    def create_analysis_tab(self):
        """建立分析頁籤"""
        with dpg.tab(label="Market Analysis"):
            dpg.add_text("Market Symbols (separate multiple with space):", color=(255, 255, 0))
            dpg.add_input_text(tag="symbols_input", hint="e.g., 2330 0050 or AAPL TSLA", width=600)
            
            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            dpg.add_text("Select Market:", color=(255, 255, 0))
            dpg.add_radio_button(
                items=[market.value.label for market in Market],
                tag="market_radio",
                default_value=Market.TAIWAN_STOCK.value.label
            )
            
            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            dpg.add_text("Select Time Interval:", color=(255, 255, 0))
            dpg.add_radio_button(
                items=[interval.value.label for interval in Interval],
                tag="interval_radio",
                default_value=Interval.ONE_DAY.value.label
            )
            
            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            dpg.add_text("Date Range (Optional):", color=(255, 255, 0))
            with dpg.group(horizontal=True):
                dpg.add_text("Start Date:")
                dpg.add_input_text(tag="start_date", hint="YYYY-MM-DD", width=150)
                dpg.add_spacer(width=20)
                dpg.add_text("End Date:")
                dpg.add_input_text(tag="end_date", hint="YYYY-MM-DD", width=150)
            
            dpg.add_spacer(height=20)
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="Start Analysis", callback=self.controller.analyze_stocks, width=150, height=40)
                dpg.add_button(label="Clear Output", callback=self.controller.clear_output, width=150, height=40)
    
    def create_database_tab(self):
        """建立資料庫管理頁籤"""
        with dpg.tab(label="Database Management"):
            dpg.add_spacer(height=20)
            dpg.add_text("Database Operations:", color=(255, 255, 0))
            dpg.add_spacer(height=10)
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="Initialize Database", callback=self.controller.init_database, width=200, height=40)
                dpg.add_text("  Create all market tables")
            
            dpg.add_spacer(height=10)
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="List Tables", callback=self.controller.list_tables, width=200, height=40)
                dpg.add_text("  Show all created tables")
    
    def create_help_tab(self):
        """建立說明頁籤"""
        with dpg.tab(label="Help"):
            dpg.add_spacer(height=10)
            dpg.add_text("Technical Indicators Analysis System", color=(0, 255, 255))
            dpg.add_spacer(height=10)
            
            dpg.add_text("Usage Steps:", color=(255, 255, 0))
            dpg.add_text("1. Enter stock symbols in 'Stock Analysis' tab")
            dpg.add_text("2. Select market type (Taiwan Stock, US Stock, etc.)")
            dpg.add_text("3. Select time interval (daily, hourly, etc.)")
            dpg.add_text("4. (Optional) Set date range")
            dpg.add_text("5. Click 'Start Analysis' button")
            
            dpg.add_spacer(height=10)
            dpg.add_text("Examples:", color=(255, 255, 0))
            dpg.add_text("  • Analyze Taiwan stock: Enter 2330, select 'Taiwan Stock (tw)' and '1 Day (1d)'")
            dpg.add_text("  • Analyze US stock: Enter AAPL, select 'US Stock (us)' and '1 Hour (1h)'")
            dpg.add_text("  • Multiple stocks: Enter 2330 0050 2454, select corresponding market and interval")
            
            dpg.add_spacer(height=10)
            dpg.add_text("Database Management:", color=(255, 255, 0))
            dpg.add_text("  • First-time users should initialize database in 'Database Management' tab")
            dpg.add_text("  • You can view created tables anytime")
    
    def create_output_section(self):
        """建立輸出區塊"""
        dpg.add_spacer(height=10)
        dpg.add_separator()
        dpg.add_spacer(height=10)
        
        dpg.add_text("Execution Results:", color=(255, 255, 0))
        dpg.add_input_text(
            tag="output_text",
            multiline=True,
            readonly=True,
            width=960,
            height=250,
            default_value=""
        )
    
    def setup_window(self):
        """設定主視窗"""
        with dpg.window(label="Technical Indicators Analysis Tool", tag="main_window", width=980, height=680):
            with dpg.tab_bar():
                self.create_analysis_tab()
                self.create_database_tab()
                self.create_help_tab()
            
            self.create_output_section()
    
    def run(self):
        """啟動GUI"""
        dpg.create_context()
        dpg.create_viewport(title='Technical Indicators Analysis Tool', width=1000, height=700)
        
        self.setup_window()
        
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()


class Controller:
    
    def clear_output(self):
        """清空輸出文字"""
        dpg.set_value("output_text", "")
    
    def append_output(self, text):
        """追加輸出文字"""
        current = dpg.get_value("output_text")
        dpg.set_value("output_text", f"{current}{text}\n")
    
    def get_user_inputs(self):
        """獲取使用者輸入"""
        symbols_text = dpg.get_value("symbols_input")
        symbols = [s.strip() for s in symbols_text.split() if s.strip()]
        
        market_selection = dpg.get_value("market_radio")
        market = next((m.value.value for m in Market if m.value.label == market_selection), None)
        
        interval_selection = dpg.get_value("interval_radio")
        interval = next((i.value.value for i in Interval if i.value.label == interval_selection), None)
        
        start_date = dpg.get_value("start_date")
        end_date = dpg.get_value("end_date")
        
        return symbols, market, interval, start_date, end_date
    
    def validate_inputs(self, symbols, market, interval):
        """驗證使用者輸入"""
        if not symbols:
            self.append_output("Please enter at least one stock symbol")
            return False
        
        if not market:
            self.append_output("Please select market type")
            return False
        
        if not interval:
            self.append_output("Please select time interval")
            return False
        
        return True
    
    def process_single_symbol(self,symbol, market, interval, start_date, end_date):
        """處理單一股票代碼"""
        try:
            self.append_output(f"\nProcessing {symbol} ({market}, {interval})...")
            
            if start_date and end_date:
                result = service.fetch_and_store_range(symbol, market, interval, start_date, end_date)
                self.append_output(f"  Date range: {start_date} ~ {end_date}")
            else:
                result = service.fetch_and_store(symbol, market, interval)
            
            self.append_output(f"✓ {symbol} technical indicator data saved successfully")
            self.append_output(f"  Fetched {result['data_count']} stock data records")
            self.append_output(f"  Calculated {result['indicator_count']} technical indicators")
            self.append_output(f"  Detected {result['pattern_count']} candlestick patterns")
            self.append_output(f"  Data saved to {market} table")
            
        except Exception as e:
            self.append_output(f"✗ Error processing {symbol}: {str(e)}")
    
    def analyze_stocks(self):
        """執行股票分析"""
        self.clear_output()
        
        symbols, market, interval, start_date, end_date = self.get_user_inputs()
        
        if not self.validate_inputs(symbols, market, interval):
            return
        
        for symbol in symbols:
            self.process_single_symbol(symbol, market, interval, start_date, end_date)
    
    def init_database(self):
        """初始化資料庫"""
        self.clear_output()
        try:
            self.append_output("Initializing database...")
            tables.create_tables()
            count = tables.get_model_count()
            self.append_output("✓ Database initialized successfully")
            self.append_output(f"  Created {count} market tables")
        except Exception as e:
            self.append_output(f"✗ Database initialization failed: {str(e)}")
    
    def list_tables(self):
        """列出所有資料表"""
        self.clear_output()
        try:
            tables_list = tables.list_all_tables()
            if tables_list:
                self.append_output(f"Database tables ({len(tables_list)} tables):")
                for i, table in enumerate(tables_list, 1):
                    self.append_output(f"  {i}. {table}")
            else:
                self.append_output("No tables in database, please initialize first")
        except Exception as e:
            self.append_output(f"✗ Failed to query tables: {str(e)}")