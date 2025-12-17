from sqlmodel import create_engine
from pathlib import Path

# SQLite 資料庫
DB_PATH = Path(__file__).parent.parent / "market_data.db"

# 建立 SQLite 引擎
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)

def getConnection():
    return engine