import csv
from typing import Dict, List
from sqlmodel import Session, select
from ..models.gacha import GachaType
from ..models.item_data import ItemData
from ..validators.item_validator import validate_csv_header, validate_item_data
from .gacha_utils import parse_gacha_types

def csv_to_json(csv_path: str, session: Session) -> List[ItemData]:
    """
    CSVファイルをItemDataのリストに変換します。

    Args:
        csv_path (str): CSVファイルのパス
        session (Session): データベースセッション

    Returns:
        List[ItemData]: 変換されたItemDataのリスト

    Raises:
        ValueError: 必須フィールドが不足している場合、または無効なデータが含まれている場合
    """
    items_data = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # ヘッダーの検証
        validate_csv_header(reader.fieldnames)

        # ガチャタイプのキャッシュを作成
        gacha_types = session.exec(select(GachaType)).all()
        gacha_type_dict = {gt.name: gt for gt in gacha_types}

        for row in reader:
            # データの検証
            validate_item_data(row, gacha_type_dict)
            # データの変換
            items_data.append(ItemData.from_csv_row(row, gacha_type_dict))
    return items_data 