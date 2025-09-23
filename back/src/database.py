"""
データベース接続とセッション管理のためのモジュール。
PostgreSQLを使用したデータベース接続の設定と、セッション管理の機能を提供します。
"""

from sqlmodel import create_engine, Session
from sqlalchemy.engine import Engine
from sqlalchemy import inspect
from .config import get_settings

def get_engine() -> Engine:
    """
    データベースエンジンのインスタンスを作成して返します。
    
    Returns:
        Engine: SQLAlchemyエンジンインスタンス
    """
    settings = get_settings()
    return create_engine(settings.database_url)

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
    テーブルが既に存在する場合は何もしません。
    アプリケーション起動時に呼び出され、必要なテーブルが存在しない場合にのみ作成します。
    """
    from sqlmodel import SQLModel
    engine = get_engine()
    
    # テーブルが既に存在するかチェック
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    # 必要なテーブル名のリスト（SQLModelのメタデータから取得）
    required_tables = SQLModel.metadata.tables.keys()
    
    # 必要なテーブルがすべて存在するかチェック
    missing_tables = [table for table in required_tables if table not in existing_tables]
    
    if missing_tables:
        # 不足しているテーブルのみ作成
        SQLModel.metadata.create_all(engine)
        return True  # テーブルを作成した
    else:
        return False  # テーブルは既に存在する
