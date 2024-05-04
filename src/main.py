import uvicorn

from src.auth.base_config import auth_backend, fastapi_users, current_user
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.operations.router import router as router_operation

from fastapi import FastAPI, Depends


# проверка перезагрузки
print(__name__)


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)


# создаём объект приложения
app = FastAPI(
    title='Trading App'
)


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


# эндпоинт, доступный для залогиненных пользователей
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


# эндпоинт, доступный для всех
@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"
