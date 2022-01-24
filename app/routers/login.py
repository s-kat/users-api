import json

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.responses import Response
from werkzeug.security import check_password_hash

from app.schemas.users import BaseInfo, LoginModel
from app.utils.auth import load_user, manager

router = APIRouter()


@router.post("/login", response_model=BaseInfo)
async def login(response: Response, data: LoginModel):
    email = data.login
    password = data.password

    user = await load_user(email)

    if not user:
        raise InvalidCredentialsException
    elif not check_password_hash(user["password"], password):
        raise InvalidCredentialsException
    access_token = manager.create_access_token(data=dict(sub=email))

    manager.set_cookie(response, access_token)

    user = dict(user.items())
    user.pop("id")
    user.pop("password")

    return user


@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse("/login", status_code=200)
    response.delete_cookie(key="access-token")
    return response
