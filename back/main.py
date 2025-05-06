from fastapi import FastAPI
from src.routes import gacha
from src.database import create_tables
from src.config import get_settings
# RV: get_settings使ってないので削除してください

app = FastAPI()

# ルーターの登録
app.include_router(gacha.router, prefix="/gacha", tags=["gacha"])

@app.on_event("startup")
# RV: on_eventは非推奨じゃないの❔
async def startup_event():
    # データベースの初期化
    create_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
    #RV: このコードって本番でも使うの❔