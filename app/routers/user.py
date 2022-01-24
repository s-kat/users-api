from fastapi import APIRouter, Depends

from app.schemas import users
from app.utils.auth import manager
from app.utils.user_utils import (change_current_user_info,
                                  get_user_private_info)

router = APIRouter()


@router.get("/users/current", response_model=users.BaseInfo)
async def get_current_user_info(user=Depends(manager)):
    info = await get_user_private_info(user["id"])
    info = dict(info.items())
    info.pop("id")
    info.pop("city")

    return info


@router.patch("/users", response_model=users.ChangedBaseUserInfo)
async def update_current_user_info(user_info: users.BaseInfo, user=Depends(manager)):
    return await change_current_user_info(user["id"], user_info)
