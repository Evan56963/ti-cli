import argparse

def build_parser():
    parser = argparse.ArgumentParser(description="Technical Indicators Analysis Tool", add_help=False)

    parser.add_argument('--gui', action='store_true', help='Launch graphical user interface (GUI)')
    parser.add_argument('--help', '-h', action='store_true', help='Show this help message and exit')

    # Create subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # add subcommand - Calculate technical indicators and detect candlestick patterns
    add_parser = subparsers.add_parser('add', help='Calculate technical indicators and detect patterns')
    add_parser.add_argument('symbols', nargs='*', help='Stock symbol list (e.g., 2330 AAPL)')
    add_parser.add_argument('--market','-m', type=str, help='Market type option', choices=['tw', 'two', 'us', 'etf', 'index', 'crypto', 'forex', 'futures'])
    add_parser.add_argument('--interval','-i', type=str, help='Time interval option', choices=['1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo'])
    add_parser.add_argument('--start', '-s', type=str, help='Start date (YYYY-MM-DD)')
    add_parser.add_argument('--end', '-e', type=str, help='End date (YYYY-MM-DD)')
    
    # db subcommand - Database management
    db_parser = subparsers.add_parser('db', help='Database management')
    db_parser.add_argument('--init', action='store_true', help='Initialize database and create all tables')
    db_parser.add_argument('--list', '-l', action='store_true', help='List all database tables')

    return parser