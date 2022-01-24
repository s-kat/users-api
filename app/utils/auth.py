from functools import wraps

from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

from app.utils.user_utils import get_user

manager = LoginManager("SECRET", token_url="/login", use_cookie=True, use_header=False)


def admin_required(fn):
    @wraps(fn)
    async def decorated_view(*args, **kwargs):
        if "user" not in kwargs or kwargs["user"]["is_admin"] is False:
            raise InvalidCredentialsException

        return await fn(*args, **kwargs)

    return decorated_view


@manager.user_loader()
async def load_user(email: str):
    return await get_user(email)
