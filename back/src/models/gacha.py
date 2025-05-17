from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional


class RarityEnum(str, Enum):
    """
    ガチャアイテムのレアリティを定義する列挙型。
    
    Attributes:
        NR: ノーマルレア
        R: レア
        SR: スーパーレア
        SSR: スーパースーパーレア
    """
    NR = "NR"
    R = "R"
    SR = "SR"
    SSR = "SSR"

class Rarity(SQLModel, table=True):
    """
    レアリティの重み付けを管理するテーブルモデル。
    
    Attributes:
        id: プライマリーキー
        name: レアリティ名（RarityEnum）
        weight: 出現確率の重み
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: RarityEnum
    weight: int

class GachaTypeItemLink(SQLModel, table=True):
    """
    ガチャタイプとアイテムの関連付けを管理する中間テーブルモデル。
    
    Attributes:
        gacha_type_id: ガチャタイプのID（外部キー）
        gacha_item_id: ガチャアイテムのID（外部キー）
        weight: 出現確率の重み
        gacha_type: 関連するガチャタイプ
        gacha_item: 関連するガチャアイテム
    """
    gacha_type_id: Optional[int] = Field(default=None, foreign_key="gachatype.id", primary_key=True)
    gacha_item_id: Optional[int] = Field(default=None, foreign_key="gachaitem.id", primary_key=True)
    weight: int

    gacha_type: "GachaType" = Relationship(back_populates="gacha_item_links")
    gacha_item: "GachaItem" = Relationship(back_populates="gacha_type_links")

class GachaType(SQLModel, table=True):
    """
    ガチャの種類を管理するテーブルモデル。
    
    Attributes:
        id: プライマリーキー
        name: ガチャタイプ名
        gacha_item_links: 関連するガチャアイテムとのリンク
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    gacha_item_links: List[GachaTypeItemLink] = Relationship(back_populates="gacha_type")

class GachaItem(SQLModel, table=True):
    """
    ガチャアイテムを管理するテーブルモデル。
    
    Attributes:
        id: プライマリーキー
        name: アイテム名
        rarity: レアリティ
        s3_key: 画像のS3オブジェクトキー
        gacha_type_links: 関連するガチャタイプとのリンク
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    rarity: RarityEnum
    s3_key: str = Field(index=True)  # S3オブジェクトキー
    gacha_type_links: List[GachaTypeItemLink] = Relationship(back_populates="gacha_item") 