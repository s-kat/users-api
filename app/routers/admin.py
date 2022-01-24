from fastapi import APIRouter, Depends

from app.schemas import users
from app.utils.auth import admin_required, manager
from app.utils.user_utils import (change_user_info, create_user, delete_user,
                                  get_user_private_info)

router = APIRouter()


@router.get("/")
async def health_check():
    return {"Hello": "World"}


@router.post(
    "/private/users", response_model=users.PrivateUserModelInfo, status_code=201
)
@admin_required
async def private_create_user(
    user_info: users.PrivateCreateUserModel, user=Depends(manager)
):
    """Creates a new user and writes it to the database"""
    return await create_user(user_info)


@router.get(
    "/private/users/{pk}", response_model=users.PrivateUserModelInfo, status_code=200
)
@admin_required
async def private_get_user_info(pk: int, user=Depends(manager)):
    return await get_user_private_info(pk)


@router.delete("/private/users/{pk}", status_code=204)
@admin_required
async def private_delete_user(pk: int, user=Depends(manager)):
    return await delete_user(pk)


@router.patch(
    "/private/users/{pk}", response_model=users.PrivateUserModelInfo, status_code=200
)
@admin_required
async def private_change_user_info(
    pk: int, user_info: users.PrivateChangeUserInfo, user=Depends(manager)
):
    return await change_user_info(pk, user_info)
