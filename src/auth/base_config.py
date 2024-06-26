from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from src.auth.manager import get_user_manager
from src.auth.models import User

from src.config import SECRETA as SECRET


# стратегия валидации и хранения аутентификации
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


# настройка куки
cookie_transport = CookieTransport(cookie_name='bonds', cookie_max_age=3600)


# настройка бэкэнда аутентификации
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


# создаём объект для работы с роутерами
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


# переменная с текщим пользователем
current_user = fastapi_users.current_user()
