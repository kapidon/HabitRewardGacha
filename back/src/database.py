"""
データベース接続とセッション管理のためのモジュール。
SQLiteを使用したデータベース接続の設定と、セッション管理の機能を提供します。

Note:
    将来的にPostgreSQLに移行する予定です。
"""

from sqlmodel import create_engine, Session
from sqlalchemy.engine import Engine
import os

def get_engine() -> Engine:
    """
    データベースエンジンのインスタンスを作成して返します。
    
    Returns:
        Engine: SQLAlchemyエンジンインスタンス
    """
    # データベースファイルのパスを取得
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "..", "database.db")
    
    # SQLiteのURL形式を修正（絶対パスを使用）
    sqlite_url = f"sqlite:///{db_path}"
    return create_engine(sqlite_url, connect_args={"check_same_thread": False})

def get_session() -> Session:
    """
    データベースセッションを作成して返します。
    
    Returns:
        Session: SQLModelセッションインスタンス
    """
    return Session(get_engine())

def create_tables():
    """
    データベースのテーブルを作成します。
    アプリケーション起動時に呼び出され、必要なテーブルが存在しない場合に作成します。
    
    Note:
        将来的にPostgreSQLに移行する予定です。
    """
    from sqlmodel import SQLModel
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
