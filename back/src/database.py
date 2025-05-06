from sqlmodel import create_engine, Session
from sqlalchemy.engine import Engine
import os

# RV: このファイルにDocstringをつけてください。どういう処理
def get_engine() -> Engine:
    # データベースファイルのパスを取得
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "..", "database.db")
    
    # SQLiteのURL形式を修正（絶対パスを使用）
    sqlite_url = f"sqlite:///{db_path}"
    return create_engine(sqlite_url, connect_args={"check_same_thread": False})

def get_session() -> Session:
    return Session(get_engine())

def create_tables():
    from sqlmodel import SQLModel
    engine = get_engine()
    SQLModel.metadata.create_all(engine) 
    # RV: postgresに変えるよって書いといて