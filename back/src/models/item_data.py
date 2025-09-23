from dataclasses import dataclass
from typing import Dict, List, Optional
from ..models.gacha import GachaType, RarityEnum
from ..utils.gacha_utils import parse_gacha_types

@dataclass
class ItemData:
    """
    ガチャアイテムのデータを表すクラス
    """
    name: str
    rarity: RarityEnum
    image_filename: str
    gacha_types: List[str]
    weight: int = 1
    blog_url: Optional[str] = None
    blog_name: Optional[str] = None
    description: Optional[str] = None

    @staticmethod
    def parse_weight(weight_str: Optional[str]) -> int:
        """
        weightフィールドの文字列を整数に変換します。
        空欄や無効な値の場合は1を返します。

        Args:
            weight_str (Optional[str]): 変換するweight文字列

        Returns:
            int: 変換されたweight値（1以上）
        """
        if weight_str is None or weight_str.strip() == '':
            return 1
        
        try:
            weight = int(weight_str)
            return max(1, weight)  # 1未満の場合は1に設定
        except ValueError:
            return 1  # 数値に変換できない場合は1に設定

    @classmethod
    def from_csv_row(cls, row: Dict[str, str], gacha_type_dict: Dict[str, GachaType]) -> 'ItemData':
        """
        CSVの行からItemDataを作成します。

        Args:
            row (Dict[str, str]): CSVの行データ
            gacha_type_dict (Dict[str, GachaType]): ガチャタイプの辞書

        Returns:
            ItemData: 作成されたItemData
        """
        return cls(
            name=row['name'],
            rarity=RarityEnum(row['rarity']),
            image_filename=row['image_filename'],
            gacha_types=parse_gacha_types(row['gacha_types']),
            weight=cls.parse_weight(row.get('weight')),
            blog_url=row.get('blog_url'),
            blog_name=row.get('blog_name'),
            description=row.get('description')
        ) 