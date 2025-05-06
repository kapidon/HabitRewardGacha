from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
import random
from ..database import get_session
from ..models.gacha import Rarity, GachaItem, GachaType, GachaTypeItemLink
from ..config import get_settings
from ..storage import get_storage_client
from ..config import get_settings


router = APIRouter()

@router.get("/pull")
async def pull(gacha_type: str, session: Session = Depends(get_session)):
    # RV: この関数にDocstringをつけてください。どういう処理
    settings = get_settings()
    storage_client = get_storage_client(settings)
    # RV: 普通はこういう処理はサービス層みたいな別のファイルだよね❔違ったらそのままで良い
    # RV: レアリティの抽選とアイテムの抽選は別の関数にした方が良いと思います。

    # レアリティの抽選
    rarities = session.exec(select(Rarity))
    rarity_dict = {rarity.name: rarity.weight for rarity in rarities}
    choiced_rarity = random.choices(list(rarity_dict.keys()), weights=list(rarity_dict.values()))[0]

    # アイテムの抽選
    items_with_weights = session.exec(
        select(GachaItem, GachaTypeItemLink.weight)
        .join(GachaTypeItemLink)
        .join(GachaType)
        .where(
            GachaType.name == gacha_type,
            GachaItem.rarity == choiced_rarity
        )
    ).all()

    if not items_with_weights:
        raise HTTPException(
            status_code=404,
            detail=f"No items found for rarity '{choiced_rarity}' in gacha type '{gacha_type}'"
        )

    # アイテムと重みを分離
    items, weights = zip(*items_with_weights)
    choiced_item = random.choices(items, weights=weights)[0]

    image_url = storage_client.get_url(choiced_item.s3_key)

    return {"name": choiced_item.name, "rarity": choiced_rarity, "image_url": image_url}