from sqlmodel import create_engine
from pathlib import Path

# SQLite database
DB_PATH = Path(__file__).parent.parent / "market_data.db"

# Create SQLite engine
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)

def get_connection():
    return engine