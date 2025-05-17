from fastapi import FastAPI
from src.routes import gacha
from src.database import create_tables

app = FastAPI()

# ルーターの登録
app.include_router(gacha.router, prefix="/gacha", tags=["gacha"])

@app.on_event("startup")
async def startup_event():
    # データベースの初期化
    create_tables()

if __name__ == "__main__":
    # 開発環境でのデバッグ用
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)