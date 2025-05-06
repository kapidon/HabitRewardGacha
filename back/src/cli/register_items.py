import argparse
import json
import os
from pathlib import Path
from typing import List, Dict
from sqlmodel import Session, select
from ..database import get_session
from ..models.gacha import GachaItem, GachaType, GachaTypeItemLink
from ..storage import get_storage_client
from ..config import get_settings

def upload_image(storage_client, image_path: str, s3_key: str) -> str:
    """画像をストレージにアップロードし、S3キーを返す"""
    with open(image_path, 'rb') as f:
        storage_client.client.upload_fileobj(f, storage_client.settings.minio_bucket, s3_key)
    return s3_key

def register_items(items_data: List[Dict], image_dir: str, session: Session):
    """アイテムと画像を一括登録する"""
    settings = get_settings()
    storage_client = get_storage_client(settings)

    # ガチャタイプのキャッシュを作成
    gacha_types = session.exec(select(GachaType)).all()
    gacha_type_dict = {gt.name: gt for gt in gacha_types}

    # アイテムとリンクのリストを準備
    items_to_create = []
    links_to_create = []
    failed_items = []

    # 画像のアップロードとアイテム情報の準備
    for item_data in items_data:
        image_path = os.path.join(image_dir, item_data['image_filename'])
        if not os.path.exists(image_path):
            print(f"警告: 画像ファイルが見つかりません: {image_path}")
            failed_items.append(item_data['name'])
            continue

        s3_key = f"items/{item_data['image_filename']}"
        try:
            upload_image(storage_client, image_path, s3_key)
        except Exception as e:
            print(f"エラー: 画像のアップロードに失敗しました: {image_path}")
            print(f"エラー詳細: {str(e)}")
            failed_items.append(item_data['name'])
            continue

        # アイテムの作成
        item = GachaItem(
            name=item_data['name'],
            rarity=item_data['rarity'],
            s3_key=s3_key
        )
        items_to_create.append(item)

    # アイテムの一括作成
    if items_to_create:
        session.add_all(items_to_create)
        session.commit()

        # リンクの作成
        for item, item_data in zip(items_to_create, items_data):
            for gacha_type_name in item_data['gacha_types']:
                gacha_type = gacha_type_dict.get(gacha_type_name)
                if gacha_type:
                    link = GachaTypeItemLink(
                        gacha_type_id=gacha_type.id,
                        gacha_item_id=item.id,
                        weight=item_data.get('weight', 1)
                    )
                    links_to_create.append(link)
                else:
                    print(f"警告: ガチャタイプが見つかりません: {gacha_type_name}")

        # リンクの一括作成
        if links_to_create:
            session.add_all(links_to_create)
            session.commit()

        print(f"登録完了: {len(items_to_create)}件のアイテム")
        if failed_items:
            print(f"登録失敗: {len(failed_items)}件")
            print("失敗したアイテム:", ", ".join(failed_items))

def main():
    parser = argparse.ArgumentParser(description='ガチャアイテムと画像を一括登録するCLIツール')
    parser.add_argument('--items-json', required=True, help='アイテム情報のJSONファイルパス')
    parser.add_argument('--image-dir', required=True, help='画像ファイルのディレクトリパス')
    args = parser.parse_args()

    # JSONファイルの読み込み
    with open(args.items_json, 'r', encoding='utf-8') as f:
        items_data = json.load(f)

    # セッションの取得と登録処理の実行
    with get_session() as session:
        register_items(items_data, args.image_dir, session)

if __name__ == '__main__':
    main() 