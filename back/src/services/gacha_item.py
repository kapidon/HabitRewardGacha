import os
from typing import Dict, List
from sqlmodel import Session, select
from ..models.gacha import GachaItem, GachaType, GachaTypeItemLink
from ..models.item_data import ItemData
from ..storage import StorageClient

class GachaItemService:
    """
    ガチャアイテムの登録を管理するサービスクラス
    """
    def __init__(self, session: Session, storage_client: StorageClient, image_dir: str):
        self.session = session
        self.storage_client = storage_client
        self.image_dir = image_dir
        self.gacha_type_dict = self._get_gacha_type_dict()

    def _get_gacha_type_dict(self) -> Dict[str, GachaType]:
        """
        ガチャタイプの辞書を取得します。

        Returns:
            Dict[str, GachaType]: ガチャタイプの辞書
        """
        gacha_types = self.session.exec(select(GachaType)).all()
        return {gt.name: gt for gt in gacha_types}

    def delete_all_items_and_links(self) -> None:
        """
        既存のアイテムとリンクをすべて削除します。

        Raises:
            Exception: 削除処理が失敗した場合
        """
        try:
            # 外部キー制約があるため、リンクを先に削除
            self.session.exec(select(GachaTypeItemLink)).delete()
            # アイテムを削除
            self.session.exec(select(GachaItem)).delete()
            self.session.commit()
            print("既存のアイテムとリンクを削除しました")
        except Exception as e:
            self.session.rollback()
            print(f"エラー: 削除処理が失敗しました: {str(e)}")
            raise

    def upload_image(self, image_filename: str) -> str:
        """
        画像をストレージにアップロードします。

        Args:
            image_filename (str): アップロードする画像のファイル名

        Returns:
            str: アップロードされた画像のS3キー
        """
        image_path = os.path.join(self.image_dir, image_filename)
        s3_key = f"items/{image_filename}"

        if not os.path.exists(image_path):
            print(f"警告: 画像ファイルが見つかりません: {image_path}")
            return ''

        try:
            with open(image_path, 'rb') as f:
                self.storage_client.client.upload_fileobj(
                    f, 
                    self.storage_client.settings.minio_bucket, 
                    s3_key
                )
            return s3_key
        except Exception as e:
            print(f"エラー: 画像のアップロードに失敗しました: {image_path}")
            print(f"エラー詳細: {str(e)}")
            return ''

    def register_items(self, items_data: List[ItemData]) -> None:
        """
        アイテムと画像を一括登録します。

        Args:
            items_data (List[ItemData]): 登録するアイテム情報のリスト

        Raises:
            Exception: トランザクションが失敗した場合
        """
        items_to_create = [
            GachaItem(
                name=item_data.name,
                rarity=item_data.rarity,
                s3_key=self.upload_image(item_data.image_filename),
                blog_url=item_data.blog_url,
                blog_name=item_data.blog_name,
                description=item_data.description
            ) for item_data in items_data
        ]

        if not items_to_create:
            return

        try:
            # アイテムの登録
            self.session.add_all(items_to_create)
            self.session.flush()  # 一時的にDBに反映してIDを取得

            # リンクの作成
            links_to_create = [
                GachaTypeItemLink(
                    gacha_type_id=self.gacha_type_dict[gacha_type_name].id,
                    gacha_item_id=item.id,
                    weight=item_data.weight
                )
                for item, item_data in zip(items_to_create, items_data)
                for gacha_type_name in item_data.gacha_types
            ]

            # リンクの一括作成
            if links_to_create:
                self.session.add_all(links_to_create)

            # 最後にまとめてコミット
            self.session.commit()
            print(f"登録完了: {len(items_to_create)}件のアイテム")
        except Exception as e:
            self.session.rollback()
            print(f"エラー: トランザクションが失敗しました: {str(e)}")
            raise

    def replace_all_items(self, items_data: List[ItemData]) -> None:
        """
        既存のアイテムとリンクを削除してから、新しいアイテムを一括登録します（完全洗い替え）。

        Args:
            items_data (List[ItemData]): 登録するアイテム情報のリスト

        Raises:
            Exception: 処理が失敗した場合
        """
        try:
            # 既存のアイテムとリンクを削除
            self.delete_all_items_and_links()
            
            # 新しいアイテムを登録
            self.register_items(items_data)
            
            print("完全洗い替えが完了しました")
        except Exception as e:
            print(f"エラー: 完全洗い替えが失敗しました: {str(e)}")
            raise 