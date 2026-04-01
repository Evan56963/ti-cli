from ti.services import MarketService
from ti.database import tables
from ti.history_msg import HistoryMsg, HistoryMsgList
from typing import TYPE_CHECKING, Callable
import uuid

if TYPE_CHECKING:
    from .components import InputComponents, OutputComponents

service = MarketService()

class Controller:
    
    def __init__(self, input_components: InputComponents, output_components: OutputComponents):
        self.input = input_components
        self.output = output_components
        self.msg_list = HistoryMsgList()
        self._refresh_msg_center: Callable[[], None] | None = None

    def set_msg_center_refresh(self, callback: Callable[[], None]) -> None:
        """Register a callback to refresh the message center UI."""
        self._refresh_msg_center = callback

    def _add_history_msg(self, msg_guid: str, is_real: bool, importance: str, is_use: str, is_read: bool) -> None:
        msg = HistoryMsg(
            uuid=str(uuid.uuid4()),
            msgGUID=msg_guid,
            isReal=is_real,
            importance=importance,
            isUse=is_use,
            isRead=is_read,
        )
        self.msg_list.add(msg)
        if self._refresh_msg_center:
            self._refresh_msg_center()

    def append(self, text: str):
        self.output.append(text)

    def clear(self):
        self.output.clear()

    def get_user_inputs(self) -> tuple[list[str], str | None, str | None, str, str]:
        """Get user inputs"""
        symbols = self.input.get_symbols()
        market = self.input.get_market()
        interval = self.input.get_interval()
        start_date, end_date = self.input.get_date_range()
        
        return symbols, market, interval, start_date, end_date
    
    def validate_inputs(self, symbols, market, interval):
        """Validate user inputs"""
        if not symbols:
            self.output.append("Please enter at least one stock symbol")
            return False
        
        if not market:
            self.output.append("Please select market type")
            return False
        
        if not interval:
            self.output.append("Please select time interval")
            return False
        
        return True
    
    def process_single_symbol(self, symbol, market, interval, start_date, end_date):
        """Process single stock symbol"""
        try:
            self.output.append(f"\nProcessing {symbol} ({market}, {interval})...")
            
            if start_date and end_date:
                result = service.fetch_and_store_range(symbol, market, interval, start_date, end_date)
                self.output.append(f"  Date range: {start_date} ~ {end_date}")
            else:
                result = service.fetch_and_store(symbol, market, interval)
            
            self.output.append(f"✓ {symbol} technical indicator data saved successfully")
            self.output.append(f"  Fetched {result['data_count']} stock data records")
            self.output.append(f"  Calculated {result['indicator_count']} technical indicators")
            self.output.append(f"  Detected {result['pattern_count']} candlestick patterns")
            self.output.append(f"  Data saved to {market} table")
            self._add_history_msg(
                msg_guid=f"{symbol}-{market}-{interval}",
                is_real=True,
                importance='0',
                is_use='1',
                is_read=False,
            )
        except Exception as e:
            self.output.append(f"✗ Error processing {symbol}: {str(e)}")
            self._add_history_msg(
                msg_guid=f"{symbol}-{market}-{interval}",
                is_real=True,
                importance='2',
                is_use='3',
                is_read=False,
            )
    
    def analyze_stocks(self):
        """Execute stock analysis"""
        self.clear()
        
        symbols, market, interval, start_date, end_date = self.get_user_inputs()
        
        if not self.validate_inputs(symbols, market, interval):
            return
        
        for symbol in symbols:
            self.process_single_symbol(symbol, market, interval, start_date, end_date)
    
    def init_database(self):
        """Initialize database"""
        self.output.clear()
        try:
            self.output.append("Initializing database...")
            tables.create_tables()
            count = tables.get_model_count()
            self.output.append("✓ Database initialized successfully")
            self.output.append(f"  Created {count} market tables")
        except Exception as e:
            self.output.append(f"✗ Database initialization failed: {str(e)}")
    
    def list_tables(self):
        """List all tables"""
        self.output.clear()
        try:
            tables_list = tables.list_all_tables()
            if tables_list:
                self.output.append(f"Database tables ({len(tables_list)} tables):")
                for i, table in enumerate(tables_list, 1):
                    self.output.append(f"  {i}. {table}")
            else:
                self.output.append("No tables in database, please initialize first")
        except Exception as e:
            self.output.append(f"✗ Failed to query tables: {str(e)}")

    def msg_center_first_page(self) -> None:
        """Navigate to first page of message center"""
        self.msg_list.go_to_first()
        if self._refresh_msg_center:
            self._refresh_msg_center()

    def msg_center_prev_page(self) -> None:
        """Navigate to previous page of message center"""
        self.msg_list.go_to_prev()
        if self._refresh_msg_center:
            self._refresh_msg_center()

    def msg_center_next_page(self) -> None:
        """Navigate to next page of message center"""
        self.msg_list.go_to_next()
        if self._refresh_msg_center:
            self._refresh_msg_center()

    def msg_center_last_page(self) -> None:
        """Navigate to last page of message center"""
        self.msg_list.go_to_last()
        if self._refresh_msg_center:
            self._refresh_msg_center()