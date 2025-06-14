from typing import Dict, List
from ..models.gacha import GachaType, RarityEnum
from ..utils.gacha_utils import parse_gacha_types

def validate_csv_header(header: List[str]) -> None:
    """
    CSVのヘッダー行を検証します。

    Args:
        header (List[str]): CSVのヘッダー行

    Raises:
        ValueError: 必須フィールドが不足している場合
    """
    required_fields = ['name', 'rarity', 'image_filename', 'gacha_types']
    if not all(field in header for field in required_fields):
        raise ValueError(f"必須フィールドが不足しています: {required_fields}")

def validate_item_data(row: Dict[str, str], gacha_type_dict: Dict[str, GachaType]) -> None:
    """
    アイテムデータを検証します。

    Args:
        row (Dict[str, str]): 検証するアイテムデータ
        gacha_type_dict (Dict[str, GachaType]): ガチャタイプの辞書

    Raises:
        ValueError: 無効なデータが含まれている場合
    """
    # レアリティの検証
    if row['rarity'] not in [r.value for r in RarityEnum]:
        raise ValueError(f"無効なレアリティです: {row['rarity']}")

    # ガチャタイプの検証
    gacha_types = parse_gacha_types(row['gacha_types'])
    missing_types = [t for t in gacha_types if t not in gacha_type_dict]
    if missing_types:
        raise ValueError(f"存在しないガチャタイプが指定されています: {', '.join(missing_types)}")

    # 重みの検証
    try:
        weight = int(row.get('weight', 1))
        if weight < 1:
            raise ValueError(f"重みは1以上である必要があります: {weight}")
    except ValueError:
        raise ValueError(f"無効な重みの値です: {row.get('weight')}") 