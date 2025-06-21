import argparse
from ..database import get_session
from ..config import get_settings
from ..storage import get_storage_client
from ..utils.csv_parser import csv_to_json
from ..services.gacha_item import GachaItemService

def main():
    """
    ガチャアイテムと画像を完全洗い替えで一括登録するCLIツール

    使用方法:
        python register_items.py --items-csv <CSVファイルパス> --image-dir <画像ディレクトリパス>

    例:
        python register_items.py --items-csv items.csv --image-dir ./images

    CSVフォーマット:
        name,rarity,image_filename,gacha_types,weight,blog_url,blog_name,description
        アイテム1,SR,item1.png,"type1,type2",1,https://example.com/blog1,ブログ記事1,アイテム1の説明
        アイテム2,R,item2.png,"type1",2,https://example.com/blog2,ブログ記事2,アイテム2の説明

    注意:
        このツールは既存のアイテムとリンクをすべて削除してから、CSVファイルの内容で完全に置き換えます。
        実行前にデータのバックアップを取ることを推奨します。
    """
    parser = argparse.ArgumentParser(description='ガチャアイテムと画像を完全洗い替えで一括登録するCLIツール')
    parser.add_argument('--items-csv', required=True, help='アイテム情報のCSVファイルパス')
    parser.add_argument('--image-dir', required=True, help='画像ファイルのディレクトリパス')
    parser.add_argument('--confirm', action='store_true', help='確認なしで実行する（デフォルトでは確認プロンプトが表示されます）')
    args = parser.parse_args()

    # 確認プロンプト（--confirmフラグがない場合）
    if not args.confirm:
        print("警告: この操作は既存のアイテムとリンクをすべて削除します。")
        print("続行しますか？ (y/N): ", end="")
        response = input().strip().lower()
        if response not in ['y', 'yes']:
            print("操作をキャンセルしました。")
            return

    try:
        with get_session() as session:
            items_data = csv_to_json(args.items_csv, session)
            settings = get_settings()
            storage_client = get_storage_client(settings)
            service = GachaItemService(session, storage_client, args.image_dir)
            
            # 完全洗い替えでアイテムを登録
            service.replace_all_items(items_data)
            
            print("完全洗い替えが正常に完了しました。")
    except Exception as e:
        print(f"エラー: {str(e)}")
        return

if __name__ == '__main__':
    main() 