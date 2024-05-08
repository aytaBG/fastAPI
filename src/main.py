from contextlib import asynccontextmanager

import uvicorn

from starlette.requests import Request
from starlette.responses import Response

from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi.staticfiles import StaticFiles

from src.auth.base_config import auth_backend, fastapi_users, current_user
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.operations.router import router as router_operation
from src.tasks.router import router as router_task
from src.pages.router import router as router_pages

from redis import asyncio as aioredis


# проверка перезагрузки
print(__name__)


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)


# создаём объект приложения
app = FastAPI(
    title='Trading App'
)


app.mount("/static", StaticFiles(directory="src/static"), name="static")


# роутер для аутентификации
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


# роутер для регистрации
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(router_operation)

app.include_router(router_task)

app.include_router(router_pages)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# эндпоинт, доступный для залогиненных пользователей
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


# эндпоинт, доступный для всех
@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"
