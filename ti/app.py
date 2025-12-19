import argparse
from ti.gui.view import Gui
from ti.services import StockDataService
from ti.utils.styles import Color, Style, stylize
from ti.database import tables
from ti.log import logger

def main():
    parser = argparse.ArgumentParser(description="Technical Indicators Analysis Tool",add_help=False)

    parser.add_argument('--gui', action='store_true', help='Launch graphical user interface (GUI)')
    parser.add_argument('--help', '-h', action='store_true', help='Show this help message and exit')

    # 建立子命令
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # add 子命令 - 計算技術指標並檢測k線型態
    add_parser = subparsers.add_parser('add', help='Calculate technical indicators and detect patterns')
    add_parser.add_argument('symbols', nargs='*', help='Stock symbol list (e.g., 2330 AAPL)')
    add_parser.add_argument('--start', '-s', type=str, help='Start date (YYYY-MM-DD)')
    add_parser.add_argument('--end', '-e', type=str, help='End date (YYYY-MM-DD)')
    add_parser.add_argument('--market','-m', type=str, help='Market type option', 
                            choices=['tw', 'two', 'us', 'etf', 'index', 'crypto', 'forex', 'futures'])
    add_parser.add_argument('--interval','-i', type=str, help='Time interval option',  
                            choices=['1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo'])
    
    # db 子命令 - 資料庫管理
    db_parser = subparsers.add_parser('db', help='Database management')
    db_parser.add_argument('--init', action='store_true', help='Initialize database and create all tables')
    db_parser.add_argument('--list', '-l', action='store_true', help='List all database tables')

    args = parser.parse_args()

    if args.gui:
        Gui().run()
        return

    if args.help or args.command is None:
        show_help()
        return
    
    # add 子命令 - 計算技術指標並分析檢測k線型態
    if args.command == 'add':
        service = StockDataService()
        
        if not args.symbols:
            logger.warning("Please provide at least one stock symbol")
            logger.warning("Example: ti add 2330 -m tw -i 1d")
            logger.warning("         ti add AAPL -m us -i 1h")
            return
        
        if not args.market:
            logger.warning("Please specify market type (e.g., -m tw, -m us, -m crypto)")
            return
        
        if not args.interval:
            logger.warning("Please specify time interval (e.g., -i 1d, -i 1h)")
            return
        

        for symbol in args.symbols:
            try:
                if args.start and args.end:
                    logger.info(f"Processing {symbol} ({args.market}, {args.interval}), date range: {args.start} ~ {args.end}")
                    result = service.fetch_and_store_range(symbol, args.market, args.interval, args.start, args.end)
                    logger.info(f"✓ {symbol} technical indicator data saved successfully")
                    logger.info(f"Retrieved {result['data_count']} stock data records")
                    logger.info(f"Calculated {result['indicator_count']} technical indicators")
                    logger.info(f"Detected {result['pattern_count']} candlestick patterns")
                    logger.info(f"Data saved to table '{args.market}'")
                else:    
                    logger.info(f"Processing {symbol} ({args.market}, {args.interval})...")
                    result = service.fetch_and_store(symbol, args.market, args.interval)
                    logger.info(f"✓ {symbol} technical indicator data saved successfully")
                    logger.info(f"Retrieved {result['data_count']} stock data records")
                    logger.info(f"Calculated {result['indicator_count']} technical indicators")
                    logger.info(f"Detected {result['pattern_count']} candlestick patterns")
                    logger.info(f"Data saved to table '{args.market}'")
                
            except:
                logger.exception(f"✗ Error occurred while processing {symbol}")
    
    # db 子命令 - 資料庫管理
    if args.command == 'db':
        if args.init:
            try:
                logger.info("Initializing database...")
                tables.create_tables()
                logger.info(f"✓ Database initialized successfully")
                logger.info(f"  Created {tables.get_model_count()} market tables")
            except:
                logger.exception("✗ Database initialization failed")
        
        elif args.list:
            try:
                table = tables.list_all_tables()
                
                if table:
                    logger.info(f"Database tables ({len(table)} tables):")
                    for i, table in enumerate(table, 1):
                        logger.info(f"  {i}. {table}")
                else:
                    logger.warning("No tables in database. Please run 'ti db --init' to initialize database")
            except:
                logger.exception("✗ Failed to query tables")
        
        else:
            logger.warning("Please specify an operation:")
            logger.warning("  --init    Initialize database and create all tables")
            logger.warning("  --list    List all database tables")
        
def show_help():
    help_text = f"""
{stylize('Technical Indicators Analysis System', Style.BOLD + Color.CYAN)}

{stylize('Basic Usage:', Style.BOLD + Color.YELLOW)}
  {stylize('ti', Color.BRIGHT_GREEN)} {stylize('[command]', Color.BRIGHT_BLUE)} {stylize('[options]', Color.BRIGHT_MAGENTA)}
  {stylize('ti --gui', Color.BRIGHT_GREEN)}                             Launch the graphical user interface (GUI)

{stylize('Subcommands:', Style.BOLD + Color.YELLOW)}
  {stylize('ti add', Color.BRIGHT_GREEN)}                               Calculate technical indicators and analyze trading signals
  {stylize('ti db', Color.BRIGHT_GREEN)}                                Database configuration and management

{stylize('Technical Analysis:', Style.BOLD + Color.YELLOW)}
  {stylize('ti add', Color.BRIGHT_GREEN)} {stylize('<stock_symbol>', Color.BRIGHT_BLUE)} {stylize('-m <market>', Color.BRIGHT_MAGENTA)} {stylize('-i <interval>', Color.BRIGHT_MAGENTA)}   Analyze stock with technical indicators

{stylize('Technical Analysis Options:', Style.BOLD + Color.YELLOW)}
  {stylize('--market, -m', Color.BRIGHT_MAGENTA)} {stylize('<market>', Color.BRIGHT_BLUE)}       Specify market type
  {stylize('--interval, -i', Color.BRIGHT_MAGENTA)} {stylize('<interval>', Color.BRIGHT_BLUE)}   Specify time interval

{stylize('Market Choices:', Style.BOLD + Color.YELLOW)}
  {stylize('tw', Color.BRIGHT_MAGENTA)}        Taiwan Stock Exchange
  {stylize('two', Color.BRIGHT_MAGENTA)}       Taiwan OTC Exchange
  {stylize('us', Color.BRIGHT_MAGENTA)}        US Stock Market
  {stylize('etf', Color.BRIGHT_MAGENTA)}       ETF
  {stylize('index', Color.BRIGHT_MAGENTA)}     Index
  {stylize('crypto', Color.BRIGHT_MAGENTA)}    Cryptocurrency
  {stylize('forex', Color.BRIGHT_MAGENTA)}     Foreign Exchange
  {stylize('futures', Color.BRIGHT_MAGENTA)}   Futures

{stylize('Time Interval Choices:', Style.BOLD + Color.YELLOW)}
  {stylize('1m', Color.BRIGHT_MAGENTA)}      1 minute data
  {stylize('5m', Color.BRIGHT_MAGENTA)}      5 minutes data
  {stylize('15m', Color.BRIGHT_MAGENTA)}     15 minutes data
  {stylize('30m', Color.BRIGHT_MAGENTA)}     30 minutes data
  {stylize('1h', Color.BRIGHT_MAGENTA)}      1 hour data
  {stylize('1d', Color.BRIGHT_MAGENTA)}      1 day data
  {stylize('1wk', Color.BRIGHT_MAGENTA)}     1 week data
  {stylize('1mo', Color.BRIGHT_MAGENTA)}     1 month data

{stylize('Date Range Options:', Style.BOLD + Color.YELLOW)}
  {stylize('-s, --start', Color.BRIGHT_MAGENTA)} {stylize('<date>', Color.BRIGHT_BLUE)}    Start date (YYYY-MM-DD format)
  {stylize('-e, --end', Color.BRIGHT_MAGENTA)} {stylize('<date>', Color.BRIGHT_BLUE)}      End date (YYYY-MM-DD format)

{stylize('Database Options:', Style.BOLD + Color.YELLOW)}
  {stylize('--init', Color.BRIGHT_GREEN)}                             Initialize database and create all tables
  {stylize('--list, -l', Color.BRIGHT_GREEN)}                         List all database tables

{stylize('Usage Examples:', Style.BOLD + Color.YELLOW)}
  {stylize('# Initialize database', Color.GRAY)}
  {stylize('ti db --init', Color.BRIGHT_GREEN)}
  
  {stylize('# Analyze Taiwan stocks', Color.GRAY)}
  {stylize('ti add 2330 -m tw -i 1d', Color.BRIGHT_GREEN)}
  {stylize('ti add 0050 --market tw --interval 1h', Color.BRIGHT_GREEN)}
  
  {stylize('# Analyze US stocks', Color.GRAY)}
  {stylize('ti add AAPL -m us -i 1d', Color.BRIGHT_GREEN)}
  {stylize('ti add TSLA --market us --interval 1h', Color.BRIGHT_GREEN)}
  
  {stylize('# Analyze multiple stocks', Color.GRAY)}
  {stylize('ti add 2330 0050 2454 -m tw -i 1d', Color.BRIGHT_GREEN)}
  {stylize('ti add AAPL MSFT GOOGL -m us -i 1d', Color.BRIGHT_GREEN)}
  
  {stylize('# Analyze with date range', Color.GRAY)}
  {stylize('ti add 2330 -m tw -i 1d -s 2024-01-01 -e 2024-12-31', Color.BRIGHT_GREEN)}
  {stylize('ti add AAPL -m us -i 1h --start 2024-06-01 --end 2024-06-30', Color.BRIGHT_GREEN)}
"""
    print(help_text)
  
if __name__ == "__main__":
    main()