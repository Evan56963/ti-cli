from dearpygui import dearpygui as dpg
from .components import InputComponents, OutputComponents, Tag, Market, Interval
from .controller import Controller

class Gui:
    """技術指標分析工具圖形介面"""

    def __init__(self):
        self.input_components = InputComponents()
        self.output_components = OutputComponents()
        self.controller = Controller(self.input_components, self.output_components)
    
    def create_analysis_tab(self):
        """建立分析頁籤"""
        with dpg.tab(label="Market Analysis"):
            dpg.add_text("Market Symbols (separate multiple with space):", color=(255, 255, 0))
            dpg.add_input_text(tag=Tag.SYMBOLS_INPUT, hint="e.g., 2330 0050 or AAPL TSLA", width=600)
            
            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            dpg.add_text("Select Market:", color=(255, 255, 0))
            dpg.add_radio_button(
                items=[market.value.label for market in Market],
                tag=Tag.MARKET_RADIO,
                default_value=Market.TAIWAN_STOCK.value.label
            )
            
            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            dpg.add_text("Select Time Interval:", color=(255, 255, 0))
            dpg.add_radio_button(
                items=[interval.value.label for interval in Interval],
                tag=Tag.INTERVAL_RADIO,
                default_value=Interval.ONE_DAY.value.label
            )
            
            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            dpg.add_text("Date Range (Optional):", color=(255, 255, 0))
            with dpg.group(horizontal=True):
                dpg.add_text("Start Date:")
                dpg.add_input_text(tag=Tag.START_DATE, hint="YYYY-MM-DD", width=150)
                dpg.add_spacer(width=20)
                dpg.add_text("End Date:")
                dpg.add_input_text(tag=Tag.END_DATE, hint="YYYY-MM-DD", width=150)
            
            dpg.add_spacer(height=20)
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="Start Analysis", callback=self.controller.analyze_stocks, width=150, height=40)
                dpg.add_button(label="Clear Output", callback=self.controller.clear, width=150, height=40)
    
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
            tag=Tag.OUTPUT_TEXT,
            multiline=True,
            readonly=True,
            width=960,
            height=250,
            default_value=""
        )
    
    def setup_window(self):
        """設定主視窗"""
        with dpg.window(label="Technical Indicators Analysis Tool", tag=Tag.MAIN_WINDOW, width=980, height=680):
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
        dpg.set_primary_window(Tag.MAIN_WINDOW, True)
        dpg.start_dearpygui()
        dpg.destroy_context()