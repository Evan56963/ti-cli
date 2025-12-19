import argparse
from ti.gui import Gui
from ti.services import StockDataService
from ti.utils.styles import Color, Style, stylize
from ti.database import tables
from ti.log import logger

def main():
    parser = argparse.ArgumentParser(description="技術指標計算與交易訊號分析工具",add_help=False)

    parser.add_argument('--gui', action='store_true', help='啟動圖形使用者介面 (GUI)')

    # 建立子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    #幫助訊息
    help_parser = subparsers.add_parser('help', help='顯示幫助訊息')

    # add 子命令 - 計算技術指標並檢測k線型態
    add_parser = subparsers.add_parser('add', help='計算技術指標並檢測k線型態')

    add_parser.add_argument('symbols', nargs='*', help='股票代碼列表 (例如: 2330 AAPL)')

    add_parser.add_argument('--market','-m', type=str, help='市場類型選項', 
                            choices=['tw', 'two', 'us', 'etf', 'index', 'crypto', 'forex', 'futures'])
    
    add_parser.add_argument('--interval','-i', type=str, help='時間間隔選項',  
                            choices=['1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo'])
    
    add_parser.add_argument('--start', '-s', type=str, help='開始日期 (YYYY-MM-DD)')
    add_parser.add_argument('--end', '-e', type=str, help='結束日期 (YYYY-MM-DD)')

    # db 子命令 - 資料庫管理
    db_parser = subparsers.add_parser('db', help='資料庫管理')

    db_parser.add_argument('--init', action='store_true', help='初始化資料庫，建立所有資料表')
    db_parser.add_argument('--list', '-l', action='store_true', help='列出當前資料庫的資料表')

    args = parser.parse_args()

    if args.gui:
        Gui().run()
        return

    if args.command == 'help' or args.command is None:
        show_help()
        return
    
    # add 子命令 - 計算技術指標並分析檢測k線型態
    if args.command == 'add':
        service = StockDataService()
        
        if not args.symbols:
            logger.warning("請提供至少一個股票代號")
            logger.warning("範例: ti add 2330 --tw --1d")
            logger.warning("      ti add AAPL --us --1h")
            return
        
        if not args.market:
            logger.warning("請指定市場類型 (例: --tw, --us, --crypto)")
            return
        
        if not args.interval:
            logger.warning("請指定時間選項 (例: --1d, --1h)")
            return
        

        for symbol in args.symbols:
            try:
                if args.start and args.end:
                    logger.info(f"正在處理 {symbol} ({args.market}, {args.interval})，日期範圍: {args.start} ~ {args.end}")
                    result = service.fetch_and_store_range(symbol, args.market, args.interval, args.start, args.end)
                    logger.info(f"✓ {symbol} 技術指標資料已成功儲存")
                    logger.info(f"獲取了 {result['data_count']} 筆股票數據")
                    logger.info(f"計算了 {result['indicator_count']} 個技術指標")
                    logger.info(f"檢測了 {result['pattern_count']} 筆K線型態資料")
                    logger.info(f"數據已保存至資料表 {args.market}")
                else:    
                    logger.info(f"正在處理 {symbol} ({args.market}, {args.interval})...")
                    result = service.fetch_and_store(symbol, args.market, args.interval)
                    logger.info(f"✓ {symbol} 技術指標資料已成功儲存")
                    logger.info(f"獲取了 {result['data_count']} 筆股票數據")
                    logger.info(f"計算了 {result['indicator_count']} 個技術指標")
                    logger.info(f"檢測了 {result['pattern_count']} 筆K線型態資料")
                    logger.info(f"數據已保存至資料表 {args.market}")
                
            except:
                logger.exception(f"✗ 處理 {symbol} 時發生錯誤")
    
    # db 子命令 - 資料庫管理
    if args.command == 'db':
        if args.init:
            try:
                logger.info("正在初始化資料庫...")
                tables.create_tables()
                logger.info(f"✓ 資料庫初始化成功")
                logger.info(f"  已建立 {tables.get_model_count()} 個市場資料表")
            except:
                logger.exception("✗ 資料庫初始化失敗")
        
        elif args.list:
            try:
                table = tables.list_all_tables()
                
                if table:
                    logger.info(f"資料庫中的資料表 ({len(table)} 個):")
                    for i, table in enumerate(table, 1):
                        logger.info(f"  {i}. {table}")
                else:
                    logger.warning("資料庫中沒有資料表，請先執行 'ti db --init' 初始化資料庫")
            except:
                logger.exception("✗ 查詢資料表失敗")
        
        else:
            logger.warning("請指定操作選項:")
            logger.warning("  --init    初始化資料庫，建立所有資料表")
            logger.warning("  --tables  列出當前資料庫的資料表")
        
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