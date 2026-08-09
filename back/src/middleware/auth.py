import secrets
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from ..config import get_settings


async def auth_middleware(request: Request, call_next):
    """
    APIキーとUser-Agentによる認証ミドルウェア
    React Nativeアプリからのアクセスのみを許可します。
    """
    settings = get_settings()
    if request.url.path == '/health':
        return await call_next(request)
    else:
        api_key = request.headers.get('X-API-Key')
        if not api_key or not secrets.compare_digest(api_key, settings.api_key):
            return JSONResponse(status_code=401, content={'error': 'Invalid API key', 'message': 'APIキーが無効です'})
        user_agent = request.headers.get('User-Agent', '')
        if not any((allowed_ua in user_agent for allowed_ua in settings.allowed_user_agents)):
            return JSONResponse(status_code=403, content={'error': 'Invalid User-Agent', 'message': '許可されていないアプリケーションです'})
        return await call_next(request)