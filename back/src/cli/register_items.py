import os
import glob
from ..database import get_session, get_engine
from ..storage import get_storage_client
from ..utils.csv_parser import csv_to_json
from ..services.gacha_item import GachaItemService
from ..config import get_settings
from sqlmodel import select
from ..models.gacha import GachaType

def main():
    """
    ガチャアイテムと画像を完全洗い替えで一括登録するCLIツール
    
    masterフォルダ内のCSVファイルを順に取り込みます。
    """
    # 固定パスの設定
    master_dir = os.path.join(os.path.dirname(__file__), '..', 'master')
    image_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'images')
    
    print(f"マスターデータディレクトリ: {master_dir}")
    print(f"画像ディレクトリ: {image_dir}")
    
    # CSVファイルの検索
    csv_pattern = os.path.join(master_dir, "*.csv")
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        print(f"CSVファイルが見つかりません: {csv_pattern}")
        return
    
    print(f"見つかったCSVファイル: {len(csv_files)}件")
    for csv_file in csv_files:
        print(f"  - {os.path.basename(csv_file)}")
    
    try:
        with get_session() as session:
            settings = get_settings()
            storage_client = get_storage_client(settings)
            service = GachaItemService(session, storage_client, image_dir)
            
            # 最初に一度だけ既存データを削除
            print("既存のアイテムとリンクを削除中...")
            service.delete_all_items_and_links()
            
            # 各CSVファイルを順に処理
            for csv_file in csv_files:
                print(f"\n処理中: {os.path.basename(csv_file)}")
                
                try:
                    # CSVファイルを読み込み
                    items_data = csv_to_json(csv_file, session)
                    print(f"  読み込み完了: {len(items_data)}件のアイテム")
                    
                    # アイテムを登録（削除は既に完了済み）
                    service.register_items(items_data)
                    print(f"  登録完了: {os.path.basename(csv_file)}")
                    
                except Exception as e:
                    print(f"  エラー: {os.path.basename(csv_file)} の処理に失敗しました: {str(e)}")
                    continue
            
            print("\nすべての処理が完了しました。")
            
    except Exception as e:
        print(f"エラー: {str(e)}")
        return

if __name__ == '__main__':
    main() 