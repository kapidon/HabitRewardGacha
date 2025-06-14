from typing import Protocol
from .config import get_settings, Settings
import boto3
from botocore.client import Config
from urllib.parse import urljoin

class StorageClient(Protocol):
    """
    ストレージサービスの抽象化インターフェース。
    異なるストレージサービス（S3, MinIO）に対して共通の操作を提供します。

    Example:
        ```python
        # 設定の取得
        settings = get_settings()
        
        # ストレージクライアントの取得
        storage_client = get_storage_client(settings)
        
        # オブジェクトのURL取得
        image_url = storage_client.get_url("images/example.jpg")
        print(image_url)  # 例: "https://example.cloudfront.net/images/example.jpg"
        ```
    """
    def get_url(self, key: str) -> str:
        """
        オブジェクトの公開URLを取得します。

        Args:
            key (str): オブジェクトのキー（パス）

        Returns:
            str: オブジェクトにアクセス可能な公開URL

        Example:
            ```python
            # オブジェクトのURLを取得
            url = storage_client.get_url("images/profile.jpg")
            print(url)  # 例: "https://example.cloudfront.net/images/profile.jpg"
            ```
        """
        ...

    def get_default_image_url(self) -> str:
        """
        デフォルト画像のURLを取得します。

        Returns:
            str: デフォルト画像のURL

        Example:
            ```python
            # デフォルト画像のURLを取得
            url = storage_client.get_default_image_url()
            print(url)  # 例: "https://example.cloudfront.net/images/default.jpg"
            ```
        """
        ...

class S3Client:
    """
    AWS S3ストレージサービスクライアント。
    本番環境で使用されるS3ストレージとのインターフェースを提供します。
    CloudFrontを使用してコンテンツを配信します。

    Example:
        ```python
        # 設定の取得
        settings = Settings()
        
        # S3クライアントの初期化
        s3_client = S3Client(settings)
        
        # オブジェクトのURL取得
        url = s3_client.get_url("images/logo.png")
        print(url)  # "https://example.cloudfront.net/images/logo.png"
        ```
    """

    def __init__(self, settings: Settings):
        """
        S3クライアントを初期化します。

        Args:
            settings (Settings): アプリケーション設定

        Example:
            ```python
            settings = Settings()
            s3_client = S3Client(settings)
            ```
        """
        self.settings = get_settings()
        # AWSのデフォルト認証情報を使用（環境変数またはIAMロール）
        self.client = boto3.client('s3')
        self.cloudfront_domain = settings.aws_cloudfront_domain
        self.default_image_key = settings.default_image_key

    def get_url(self, key: str) -> str:
        """
        CloudFront経由のオブジェクトURLを生成します。

        Args:
            key (str): S3オブジェクトのキー

        Returns:
            str: CloudFrontドメインを使用した公開URL

        Example:
            ```python
            url = s3_client.get_url("images/banner.jpg")
            print(url)  # "https://example.cloudfront.net/images/banner.jpg"
            ```
        """
        if not key:
            return self.get_default_image_url()
        return f"https://{self.cloudfront_domain}/{key}"

    def get_default_image_url(self) -> str:
        return f"https://{self.cloudfront_domain}/{self.default_image_key}"

class MinioClient:
    """
    MinIOストレージサービスクライアント。
    ローカル開発環境で使用されるMinIOストレージとのインターフェースを提供します。
    S3互換のAPIを使用して、ローカルでS3と同様の環境を構築できます。

    Example:
        ```python
        # 設定の取得
        settings = get_settings()
        
        # MinIOクライアントの初期化
        minio_client = MinioClient(settings)
        
        # オブジェクトのURL取得
        url = minio_client.get_url("images/avatar.png")
        print(url)  # "http://localhost:9000/gacha/images/avatar.png"
        ```
    """

    def __init__(self, settings: Settings):
        """
        MinIOクライアントを初期化します。

        Args:
            settings (Settings): アプリケーション設定

        Example:
            ```python
            settings = Settings()
            minio_client = MinioClient(settings)
            ```
        """
        self.settings = get_settings()
        # MinIOはS3互換のAPIを提供するため、boto3のS3クライアントを使用
        self.client = boto3.client(
            's3',
            endpoint_url=settings.minio_endpoint,  # MinIOサーバーのエンドポイント
            aws_access_key_id=settings.minio_access_key,  # MinIOのアクセスキー
            aws_secret_access_key=settings.minio_secret_key,  # MinIOのシークレットキー
            config=Config(signature_version='s3v4'),  # S3 v4署名を使用
        )
        self.default_image_key = settings.default_image_key

    def get_url(self, key: str) -> str:
        """
        MinIOサーバー経由のオブジェクトURLを生成します。

        Args:
            key (str): MinIOオブジェクトのキー

        Returns:
            str: MinIOサーバーのエンドポイントを使用した公開URL

        Example:
            ```python
            url = minio_client.get_url("images/background.jpg")
            print(url)  # "http://localhost:9000/gacha/images/background.jpg"
            ```
        """
        if not key:
            return self.get_default_image_url()
        return urljoin(self.settings.minio_endpoint, f"/{self.settings.minio_bucket}/{key}")

    def get_default_image_url(self) -> str:
        return urljoin(self.settings.minio_endpoint, f"/{self.settings.minio_bucket}/{self.default_image_key}")

def get_storage_client(settings: Settings) -> StorageClient:
    """
    環境設定に基づいて適切なストレージクライアントを取得します。

    Args:
        settings (Settings): アプリケーション設定

    Returns:
        StorageClient: 設定に応じたストレージクライアント（S3ClientまたはMinioClient）

    Note:
        - 本番環境（storage_type="s3"）: S3Clientを返します
        - ローカル環境（storage_type="minio"）: MinioClientを返します

    Example:
        ```python
        # 設定の取得
        settings = Settings(
            storage_type="minio",  # または "s3"
            # S3設定
            aws_s3_bucket="my-bucket",
            aws_cloudfront_domain="example.cloudfront.net",
            # MinIO設定
            minio_endpoint="http://localhost:9000",
            minio_access_key="minioadmin",
            minio_secret_key="minioadmin",
            minio_bucket="gacha"
        )
        
        # 適切なクライアントの取得
        storage_client = get_storage_client(settings)
        
        # オブジェクトのURL取得
        url = storage_client.get_url("images/example.jpg")
        print(url)  # 環境に応じて異なるURLが返される
        ```
    """
    if settings.storage_type == "s3":
        return S3Client(settings)
    else:
        return MinioClient(settings) 