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

    # 市場選項
    add_parser.add_argument('symbols', nargs='*', help='股票代碼列表 (例如: 2330 AAPL)')
    add_parser.add_argument('--tw', action='store_true', help='台股市場')
    add_parser.add_argument('--two', action='store_true', help='台灣櫃買市場')
    add_parser.add_argument('--us', action='store_true', help='美股市場')
    add_parser.add_argument('--etf', action='store_true', help='ETF')
    add_parser.add_argument('--index', action='store_true', help='指數')
    add_parser.add_argument('--crypto', action='store_true', help='加密貨幣')
    add_parser.add_argument('--forex', action='store_true', help='外匯')
    add_parser.add_argument('--futures', action='store_true', help='期貨')

    # 時間選項
    add_parser.add_argument('--1m', dest='m1', action='store_true', help='1 分鐘數據')
    add_parser.add_argument('--5m', dest='m5', action='store_true', help='5 分鐘數據')
    add_parser.add_argument('--15m', dest='m15', action='store_true', help='15 分鐘數據')
    add_parser.add_argument('--30m', dest='m30', action='store_true', help='30 分鐘數據')
    add_parser.add_argument('--1h', dest='h1', action='store_true', help='1 小時數據')
    add_parser.add_argument('--1d', dest='d1', action='store_true', help='1 天數據')
    add_parser.add_argument('--1wk', dest='wk1', action='store_true', help='1 週數據')
    add_parser.add_argument('--1mo', dest='mo1', action='store_true', help='1 月數據')
    add_parser.add_argument('--start', type=str, help='開始日期 (YYYY-MM-DD)')
    add_parser.add_argument('--end', type=str, help='結束日期 (YYYY-MM-DD)')

    # db 子命令 - 資料庫管理
    db_parser = subparsers.add_parser('db', help='資料庫管理')
    db_parser.add_argument('--init', action='store_true', help='初始化資料庫，建立所有資料表')
    db_parser.add_argument('--tables', action='store_true', help='列出當前資料庫的資料表')

    args = parser.parse_args()

    if args.gui:
        Gui().run()
        return

    if args.command == 'help' or args.command is None:
        show_help()
        return
    
    # 處理 add 子命令 - 計算技術指標並分析檢測k線型態
    if args.command == 'add':
        service = StockDataService()
        
        if not args.symbols:
            logger.warning("請提供至少一個股票代號")
            logger.warning("範例: ti add 2330 --tw --1d")
            logger.warning("      ti add AAPL --us --1h")
            return

        # 確定市場類型
        market = None
        if args.tw:
            market = 'tw'
        elif args.two:
            market = 'two'
        elif args.us:
            market = 'us'
        elif args.etf:
            market = 'etf'
        elif args.index:
            market = 'index'
        elif args.crypto:
            market = 'crypto'
        elif args.forex:
            market = 'forex'
        elif args.futures:
            market = 'futures'
        else:
            logger.warning("請指定市場類型 (例: --tw, --us, --crypto)")
            return
        
        # 確定時間選項
        interval = None
        if args.m1:
            interval = '1m'
        elif args.m5:
            interval = '5m'
        elif args.m15:
            interval = '15m'
        elif args.m30:
            interval = '30m'
        elif args.h1:
            interval = '1h'
        elif args.d1:
            interval = '1d'
        elif args.wk1:
            interval = '1wk'
        elif args.mo1:
            interval = '1mo'
        else:
            logger.warning("請指定時間選項 (例: --1d, --1h)")
            return
        
        for symbol in args.symbols:
            try:
                if args.start and args.end:
                    logger.info(f"正在處理 {symbol} ({market}, {interval})，日期範圍: {args.start} ~ {args.end}")
                    result = service.fetch_and_store_range(symbol, market, interval, args.start, args.end)
                    logger.info(f"✓ {symbol} 技術指標資料已成功儲存")
                    logger.info(f"獲取了 {result['data_count']} 筆股票數據")
                    logger.info(f"計算了 {result['indicator_count']} 個技術指標")
                    logger.info(f"檢測了 {result['pattern_count']} 筆K線型態資料")
                    logger.info(f"數據已保存至資料表 {market}")
                else:    
                    logger.info(f"正在處理 {symbol} ({market}, {interval})...")
                    result = service.fetch_and_store(symbol, market, interval)
                    logger.info(f"✓ {symbol} 技術指標資料已成功儲存")
                    logger.info(f"獲取了 {result['data_count']} 筆股票數據")
                    logger.info(f"計算了 {result['indicator_count']} 個技術指標")
                    logger.info(f"檢測了 {result['pattern_count']} 筆K線型態資料")
                    logger.info(f"數據已保存至資料表 {market}")
                
            except:
                logger.exception(f"✗ 處理 {symbol} 時發生錯誤")
    
    # 處理 db 子命令 - 資料庫管理
    if args.command == 'db':
        if args.init:
            try:
                logger.info("正在初始化資料庫...")
                tables.create_tables()
                logger.info(f"✓ 資料庫初始化成功")
                logger.info(f"  已建立 {tables.get_model_count()} 個市場資料表")
            except:
                logger.exception("✗ 資料庫初始化失敗")
        
        elif args.tables:
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

{stylize('Subcommands:', Style.BOLD + Color.YELLOW)}
  {stylize('ti add', Color.BRIGHT_GREEN)}                               Calculate technical indicators and analyze trading signals
  {stylize('ti db', Color.BRIGHT_GREEN)}                                Database configuration and management
{stylize('Technical Analysis:', Style.BOLD + Color.YELLOW)}
  {stylize('ti add', Color.BRIGHT_GREEN)} {stylize('<stock_symbol>', Color.BRIGHT_BLUE)} {stylize('--<market>', Color.BRIGHT_MAGENTA)} {stylize('--<interval>', Color.BRIGHT_MAGENTA)}   Analyze stock with technical indicators

{stylize('Market Options:', Style.BOLD + Color.YELLOW)}
  {stylize('--tw', Color.BRIGHT_MAGENTA)}          Taiwan Stock Exchange
  {stylize('--us', Color.BRIGHT_MAGENTA)}          US Stock Market
  {stylize('--etf', Color.BRIGHT_MAGENTA)}         ETF
  {stylize('--index', Color.BRIGHT_MAGENTA)}       Index
  {stylize('--crypto', Color.BRIGHT_MAGENTA)}      Cryptocurrency
  {stylize('--forex', Color.BRIGHT_MAGENTA)}       Foreign Exchange
  {stylize('--futures', Color.BRIGHT_MAGENTA)}     Futures
{stylize('Time Intervals:', Style.BOLD + Color.YELLOW)}
  {stylize('--1m', Color.BRIGHT_MAGENTA)}          1 minute data
  {stylize('--5m', Color.BRIGHT_MAGENTA)}          5 minutes data
  {stylize('--15m', Color.BRIGHT_MAGENTA)}         15 minutes data
  {stylize('--30m', Color.BRIGHT_MAGENTA)}         30 minutes data
  {stylize('--1h', Color.BRIGHT_MAGENTA)}          1 hour data
  {stylize('--1d', Color.BRIGHT_MAGENTA)}          1 day data
  {stylize('--1wk', Color.BRIGHT_MAGENTA)}         1 week data
  {stylize('--1mo', Color.BRIGHT_MAGENTA)}         1 month data
{stylize('Date Range Options:', Style.BOLD + Color.YELLOW)}
  {stylize('--start', Color.BRIGHT_MAGENTA)} {stylize('<date>', Color.BRIGHT_BLUE)}       Start date (YYYY-MM-DD format)
  {stylize('--end', Color.BRIGHT_MAGENTA)} {stylize('<date>', Color.BRIGHT_BLUE)}         End date (YYYY-MM-DD format)
{stylize('Database Management:', Style.BOLD + Color.YELLOW)}
  {stylize('ti db --init', Color.BRIGHT_GREEN)}                         Initialize database and create all tables
  {stylize('ti db --tables', Color.BRIGHT_GREEN)}                       List all database tables

{stylize('Usage Examples:', Style.BOLD + Color.YELLOW)}
  {stylize('# Initialize database', Color.GRAY)}
  {stylize('ti db --init', Color.BRIGHT_GREEN)}
  
  {stylize('# Analyze Taiwan stocks', Color.GRAY)}
  {stylize('ti add 2330 --tw --1d', Color.BRIGHT_GREEN)}
  {stylize('ti add 0050 --tw --1h', Color.BRIGHT_GREEN)}
  
  {stylize('# Analyze US stocks', Color.GRAY)}
  {stylize('ti add AAPL --us --1d', Color.BRIGHT_GREEN)}
  {stylize('ti add TSLA --us --1h', Color.BRIGHT_GREEN)}
  
  {stylize('# Analyze multiple stocks', Color.GRAY)}
  {stylize('ti add 2330 0050 2454 --tw --1d', Color.BRIGHT_GREEN)}
  {stylize('ti add AAPL MSFT GOOGL --us --1d', Color.BRIGHT_GREEN)}
  
  {stylize('# Analyze with date range', Color.GRAY)}
  {stylize('ti add 2330 --tw --1d --start 2024-01-01 --end 2024-12-31', Color.BRIGHT_GREEN)}
  {stylize('ti add AAPL --us --1h --start 2024-06-01 --end 2024-06-30', Color.BRIGHT_GREEN)}
"""
    print(help_text)

if __name__ == "__main__":
    main()