import argparse
from ..database import get_session
from ..config import get_settings
from ..storage import get_storage_client
from ..utils.csv_parser import csv_to_json
from ..services.gacha_item import GachaItemService

def main():
    """
    ガチャアイテムと画像を一括登録するCLIツール

    使用方法:
        python register_items.py --items-csv <CSVファイルパス> --image-dir <画像ディレクトリパス>

    例:
        python register_items.py --items-csv items.csv --image-dir ./images

    CSVフォーマット:
        name,rarity,image_filename,gacha_types,weight
        アイテム1,SR,item1.png,"type1,type2",1
        アイテム2,R,item2.png,"type1",2
    """
    parser = argparse.ArgumentParser(description='ガチャアイテムと画像を一括登録するCLIツール')
    parser.add_argument('--items-csv', required=True, help='アイテム情報のCSVファイルパス')
    parser.add_argument('--image-dir', required=True, help='画像ファイルのディレクトリパス')
    args = parser.parse_args()

    try:
        with get_session() as session:
            items_data = csv_to_json(args.items_csv, session)
            settings = get_settings()
            storage_client = get_storage_client(settings)
            service = GachaItemService(session, storage_client, args.image_dir)
            service.register_items(items_data)
    except Exception as e:
        print(f"エラー: {str(e)}")
        return

if __name__ == '__main__':
    main() 