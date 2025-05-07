from fastapi import FastAPI
from src.routes import gacha
from src.database import create_tables
# RV: get_settings使ってないので削除してください
# 回答: はい、未使用のインポートを削除します

app = FastAPI()

# ルーターの登録
app.include_router(gacha.router, prefix="/gacha", tags=["gacha"])

@app.on_event("startup")
# RV: on_eventは非推奨じゃないの❔
# 回答: FastAPIの最新バージョンでもon_eventは推奨された方法です。
# アプリケーションの起動時に一度だけ実行する必要のある初期化処理に使用されます。
async def startup_event():
    # データベースの初期化
    create_tables()

if __name__ == "__main__":
    # 開発環境でのデバッグ用
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
    #RV: このコードって本番でも使うの❔
    # 回答: いいえ、このコードは開発環境でのデバッグ用です。
    # 本番環境では通常、GunicornなどのWSGIサーバーを使用します。
    # 修正案: 以下のように開発環境用であることを明示するコメントを追加します
    # 開発環境でのデバッグ用。本番環境ではGunicornなどのWSGIサーバーを使用してください。