from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy import delete
from ..models.gacha import Rarity, RarityEnum, GachaType, GachaTypeItemLink, GachaItem
from ..config import get_settings

def init_db():
    """
    データベースを初期化し、初期データを追加します。
    """
    settings = get_settings()
    engine = create_engine(settings.database_url)

    # テーブルの作成
    SQLModel.metadata.create_all(engine)

    # セッションの作成
    with Session(engine) as session:
        try:
            # 既存のデータを削除（外部キー制約を考慮した順序）
            # 一気に削除
            session.exec(delete(GachaTypeItemLink))
            session.exec(delete(GachaItem))
            session.exec(delete(GachaType))
            session.exec(delete(Rarity))

            # レアリティの初期データ
            rarities = [
                Rarity(name=RarityEnum.SSR, weight=3),
                Rarity(name=RarityEnum.SR, weight=27),
                Rarity(name=RarityEnum.R, weight=70),
            ]
            session.add_all(rarities)

            # ガチャタイプの初期データ
            gacha_types = [
                GachaType(name="diet_food"),
            ]
            session.add_all(gacha_types)

            # すべての処理が成功した場合のみコミット
            session.commit()
            print("データベースの初期化が完了しました。")
        except Exception as e:
            # エラーが発生した場合はロールバック
            session.rollback()
            print(f"エラーが発生しました: {str(e)}")
            raise

if __name__ == "__main__":
    init_db() 