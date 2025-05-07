from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..config import get_settings
from ..storage import get_storage_client
from ..services.gacha import pull_gacha

router = APIRouter()

@router.get("/pull")
async def pull(gacha_type: str, session: Session = Depends(get_session)):
    # RV: この関数にDocstringをつけてください。どういう処理
    # 回答: はい、Docstringを追加します。
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

    settings = get_settings()
    storage_client = get_storage_client(settings)

    try:
        result = pull_gacha(session, gacha_type, storage_client)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))