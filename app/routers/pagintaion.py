from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from app.schemas.users import PrivateUserModelInfo, ShortUserInfo
from app.utils.auth import admin_required, manager
from app.utils.user_utils import (get_full_user_info_paginate,
                                  get_short_user_info_paginate)

router = APIRouter()


@router.get("/users", response_model=Page[ShortUserInfo])
async def get_short_users_info(params: Params = Depends(), user=Depends(manager)):
    return await get_short_user_info_paginate(params)


@router.get("/private/users/", response_model=Page[PrivateUserModelInfo])
@admin_required
async def get_full_users_info(params: Params = Depends(), user=Depends(manager)):
    ans = await get_full_user_info_paginate(params)
    return ans
