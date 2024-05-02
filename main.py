from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers


# создаём объект приложения
app = FastAPI(
    title='Trading App'
)


# создаём объект для работы с роутерами
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
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


# переменная с текщим пользователем
current_user = fastapi_users.current_user()


# роутер, доступный для залогиненных пользователей
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


# роутер, доступный для всех
@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"
