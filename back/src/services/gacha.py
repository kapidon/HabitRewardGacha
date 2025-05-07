"""
ガチャのビジネスロジックを管理するサービスモジュール。
抽選ロジックやデータベース操作を担当します。

Note:
    # RV: 普通はこういう処理はサービス層みたいな別のファイルだよね❔違ったらそのままで良い
    # 回答: はい、その通りです。ビジネスロジックはサービス層に分離するべきです。
    # 修正案: 以下のような構造に変更することを推奨します：
    # - src/services/gacha.py: ガチャの抽選ロジック
    # - src/routes/gacha.py: ルーティングとリクエスト/レスポンスの処理
    
    # RV: レアリティの抽選とアイテムの抽選は別の関数にした方が良いと思います。
    # 回答: はい、その通りです。責務を分離することで、コードの可読性と保守性が向上します。
    # 修正案: 以下のような関数に分割することを推奨します：
    # - draw_rarity(): レアリティの抽選
    # - draw_item(): アイテムの抽選
"""

from sqlmodel import Session, select
import random
from typing import Tuple, List
from ..models.gacha import Rarity, GachaItem, GachaType, GachaTypeItemLink
from ..storage import StorageClient

def draw_rarity(session: Session) -> str:
    """
    レアリティを抽選します。

    Args:
        session (Session): データベースセッション

    Returns:
        str: 抽選されたレアリティ名
    """
    rarities = session.exec(select(Rarity))
    rarity_dict = {rarity.name: rarity.weight for rarity in rarities}
    return random.choices(list(rarity_dict.keys()), weights=list(rarity_dict.values()))[0]

def draw_item(session: Session, gacha_type: str, rarity: str) -> GachaItem:
    """
    指定されたガチャタイプとレアリティからアイテムを抽選します。

    Args:
        session (Session): データベースセッション
        gacha_type (str): ガチャタイプ名
        rarity (str): レアリティ名

    Returns:
        GachaItem: 抽選されたアイテム

    Raises:
        ValueError: 指定された条件でアイテムが見つからない場合
    """
    items_with_weights = session.exec(
        select(GachaItem, GachaTypeItemLink.weight)
        .join(GachaTypeItemLink)
        .join(GachaType)
        .where(
            GachaType.name == gacha_type,
            GachaItem.rarity == rarity
        )
    ).all()

    if not items_with_weights:
        raise ValueError(f"No items found for rarity '{rarity}' in gacha type '{gacha_type}'")

    items, weights = zip(*items_with_weights)
    return random.choices(items, weights=weights)[0]

def pull_gacha(session: Session, gacha_type: str, storage_client: StorageClient) -> dict:
    """
    ガチャを引いて結果を返します。

    Args:
        session (Session): データベースセッション
        gacha_type (str): ガチャタイプ名
        storage_client (StorageClient): ストレージクライアント

    Returns:
        dict: 抽選結果（アイテム名、レアリティ、画像URL）

    Raises:
        ValueError: 指定された条件でアイテムが見つからない場合
    """
    # レアリティの抽選
    choiced_rarity = draw_rarity(session)

    # アイテムの抽選
    choiced_item = draw_item(session, gacha_type, choiced_rarity)

    # 画像URLの取得
    image_url = storage_client.get_url(choiced_item.s3_key)

    return {
        "name": choiced_item.name,
        "rarity": choiced_rarity,
        "image_url": image_url
    } 