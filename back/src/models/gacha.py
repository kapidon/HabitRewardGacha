from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional

# RV: 各クラスにDocstringをつけてください
class RarityEnum(str, Enum):
    NR = "NR"
    R = "R"
    SR = "SR"
    SSR = "SSR"

class Rarity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: RarityEnum
    weight: int

class GachaTypeItemLink(SQLModel, table=True):
    gacha_type_id: Optional[int] = Field(default=None, foreign_key="gachatype.id", primary_key=True)
    gacha_item_id: Optional[int] = Field(default=None, foreign_key="gachaitem.id", primary_key=True)
    weight: int

    gacha_type: "GachaType" = Relationship(back_populates="gacha_item_links")
    gacha_item: "GachaItem" = Relationship(back_populates="gacha_type_links")

class GachaType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    gacha_item_links: List[GachaTypeItemLink] = Relationship(back_populates="gacha_type")

class GachaItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    rarity: RarityEnum
    s3_key: str = Field(index=True)  # S3オブジェクトキー
    gacha_type_links: List[GachaTypeItemLink] = Relationship(back_populates="gacha_item") 