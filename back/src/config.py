from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    """
    アプリケーションの設定を管理するクラス。
    環境変数から設定を読み込み、型安全な方法でアクセスできるようにします。

    Attributes:
        storage_type (Literal["s3", "minio"]): 使用するストレージサービスの種類
            - "s3": 本番環境用のAWS S3
            - "minio": ローカル開発環境用のMinIO

        # AWS S3設定
        aws_s3_bucket (str): S3バケット名
        aws_cloudfront_domain (str): CloudFrontのドメイン名

        # MinIO設定
        minio_endpoint (str): MinIOサーバーのエンドポイントURL
        minio_access_key (str): MinIOのアクセスキー
        minio_secret_key (str): MinIOのシークレットキー
        minio_bucket (str): MinIOのバケット名

        # デフォルト画像設定
        default_image_key (str): デフォルト画像のS3キー
    """

    # ストレージタイプ設定
    storage_type: Literal["s3", "minio"] = "s3"

    # AWS S3設定
    aws_s3_bucket: str
    aws_cloudfront_domain: str

    # MinIO設定（デフォルト値はMinIOの標準設定）
    minio_endpoint: str = "http://localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "gacha"

    # デフォルト画像設定
    default_image_key: str = "images/default.png"

    # 設定の読み込み方法を指定
    model_config = SettingsConfigDict(
        env_file=".env",  # ローカル環境では.envファイルから読み込み
        env_file_encoding="utf-8"  # ファイルのエンコーディング
    )

def get_settings() -> Settings:
    """
    アプリケーション設定を取得します。

    Returns:
        Settings: 環境変数から読み込まれた設定オブジェクト

    Note:
        - ローカル環境: .envファイルから設定を読み込みます
        - 本番環境: 環境変数から直接設定を読み込みます
    """
    return Settings() 