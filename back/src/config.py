from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, List

class Settings(BaseSettings):
    """
    アプリケーションの設定を管理するクラス。
    環境変数から設定を読み込み、型安全な方法でアクセスできるようにします。

    設定の優先順位:
    1. 環境変数（本番環境: Render、開発環境: 手動設定）
    2. .envファイル（ローカル開発環境のみ）

    Attributes:
        environment (Literal["development", "production"]): 実行環境
            - "development": ローカル開発環境（/docsなどのAPIドキュメントを公開）
            - "production": 本番環境（/docsなどのAPIドキュメントを非公開）

        storage_type (Literal["s3", "minio"]): 使用するストレージサービスの種類
            - "s3": 本番環境用のAWS S3
            - "minio": ローカル開発環境用のMinIO

        # AWS S3設定
        aws_s3_bucket (str): S3バケット名
        aws_cloudfront_domain (str): CloudFrontのドメイン名

        # MinIO設定
        minio_endpoint (str): MinIOサーバーのエンドポイントURL
        minio_access_key (str): MinIOのアクセスキー（.envファイルまたは環境変数から設定）
        minio_secret_key (str): MinIOのシークレットキー（.envファイルまたは環境変数から設定）
        minio_bucket (str): MinIOのバケット名

        # データベース設定
        database_url (str): データベース接続URL

        # CORS設定
        allowed_origins (List[str]): 許可するオリジンのリスト
            - "*": すべてのオリジンを許可（React Nativeネイティブアプリ用）
            - 特定のドメイン: Webアプリ用

        # 認証設定
        api_key (str): APIキー（React Nativeアプリからのアクセス認証用）
        allowed_user_agents (List[str]): 許可するUser-Agentのリスト
    """

    # 実行環境設定
    environment: Literal["development", "production"] = "development"

    # ストレージタイプ設定
    storage_type: Literal["s3", "minio"] = "s3"

    # AWS S3設定
    aws_s3_bucket: str
    aws_cloudfront_domain: str

    # MinIO設定（アクセスキー・シークレットキーは環境変数から必須で設定）
    minio_endpoint: str = "http://localhost:9000"
    minio_access_key: str = ""
    minio_secret_key: str = ""
    minio_bucket: str = "gacha"

    # データベース設定
    database_url: str

    # CORS設定
    allowed_origins: List[str] = [
        # React Nativeネイティブアプリ用（すべてのオリジンを許可）
        "*",
    ]

    # 認証設定
    api_key: str  # 環境変数から必須で設定
    allowed_user_agents: List[str] = [
        # React NativeアプリのUser-Agent
        "RewardGacha/1.0",
        # 開発環境用（必要に応じて）
        "okhttp/4.9.0",
        "axios/1.0.0",
    ]

    # 設定の読み込み方法を指定
    model_config = SettingsConfigDict(
        env_file=".env",  # ローカル環境では.envファイルから読み込み
        env_file_encoding="utf-8",  # ファイルのエンコーディング
        case_sensitive=False  # 環境変数名の大文字小文字を区別しない
    )

def get_settings() -> Settings:
    """
    アプリケーション設定を取得します。

    Returns:
        Settings: 環境変数から読み込まれた設定オブジェクト

    Note:
        - 本番環境（Render）: 環境変数から直接設定を読み込みます
        - ローカル環境: .envファイルから設定を読み込みます（環境変数が設定されていない場合）
        - 環境変数が設定されている場合は、.envファイルよりも優先されます
        - API_KEYは必須の環境変数です
    """
    return Settings() 