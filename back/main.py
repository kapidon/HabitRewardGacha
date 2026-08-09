from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import gacha
from src.database import create_tables
from src.config import get_settings
from src.middleware.auth import auth_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    アプリケーションのライフサイクルを管理します。
    本番環境（Render）とローカル開発環境の両方で動作します。
    コールドスリープ後の起動にも対応します。
    """
    try:
        # アプリケーション起動時の処理
        print("アプリケーション起動中...")
        
        # テーブル作成（既存の場合は何もしない）
        tables_created = create_tables()
        if tables_created:
            print("データベーステーブルを作成しました")
        else:
            print("データベーステーブルは既に存在します")
            
    except Exception as e:
        print(f"起動時のエラー: {e}")
        # エラーが発生してもアプリケーションは起動を続行
        # データベース接続は初回リクエスト時に再試行される
    
    yield
    
    # アプリケーション終了時の処理（必要に応じて追加）
    print("アプリケーション終了中...")

settings = get_settings()
is_production = settings.environment == "production"

app = FastAPI(
    lifespan=lifespan,
    title="RewardGacha API",
    description="ガチャシステムのAPI",
    version="1.0.0",
    # 本番環境ではAPIドキュメントを非公開にする
    docs_url=None if is_production else "/docs",
    redoc_url=None if is_production else "/redoc",
    openapi_url=None if is_production else "/openapi.json",
)

# CORS設定
# React Nativeネイティブアプリからのアクセスが前提でCookieを使用しないため、
# allow_credentials=Falseとする（allow_origins=["*"]との併用はブラウザ仕様上矛盾するため）
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 認証ミドルウェアを追加
app.middleware("http")(auth_middleware)

# ルーターの登録
app.include_router(gacha.router, prefix="/gacha", tags=["gacha"])

@app.get("/health")
async def health_check():
    """
    ヘルスチェックエンドポイント
    コールドスリープ後の起動確認用
    """
    return {"status": "healthy", "message": "アプリケーションが正常に動作しています"}

if __name__ == "__main__":
    # ローカル開発環境でのデバッグ用
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)