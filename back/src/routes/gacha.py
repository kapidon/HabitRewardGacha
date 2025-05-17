from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..config import get_settings
from ..storage import get_storage_client
from ..services.gacha import pull_gacha

router = APIRouter()

@router.get("/pull")
async def pull(gacha_type: str, session: Session = Depends(get_session)):
    """
    指定されたガチャタイプからアイテムを1つ抽選します。
    
    Args:
        gacha_type (str): 抽選するガチャのタイプ
        session (Session): データベースセッション
    
    Returns:
        dict: 抽選結果（アイテム名、レアリティ、画像URL）
    
    Raises:
        HTTPException: 指定されたガチャタイプとレアリティの組み合わせでアイテムが見つからない場合
    """
    settings = get_settings()
    storage_client = get_storage_client(settings)

    try:
        result = pull_gacha(session, gacha_type, storage_client)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))