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
            weight=int(row.get('weight', 1)),
            blog_url=row.get('blog_url')
        ) 