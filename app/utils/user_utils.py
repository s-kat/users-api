import databases
from fastapi import HTTPException
from fastapi_pagination import Params
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import delete, select, update
from werkzeug.security import generate_password_hash

from app.models.database import database
from app.models.users import users
from app.schemas.users import (BaseInfo, PrivateCreateUserModel,
                               PrivateUserModelInfo)
from app.utils.error_handlers import (check_if_user_email_exists,
                                      check_if_user_id_exists)


def hash_password(password: str):
    return generate_password_hash(password)


async def create_user(user: PrivateCreateUserModel):
    """Creates new user in database"""
    await check_if_user_email_exists(email=user.email)

    hashed_password = hash_password(user.password)
    user.dict().pop("password")

    query = users.insert().values(
        first_name=user.first_name,
        last_name=user.last_name,
        other_name=user.other_name,
        email=user.email,
        phone=user.phone,
        birthday=user.birthday,
        city=user.city,
        additional_info=user.additional_info,
        is_admin=user.is_admin,
        password=hashed_password,
    )
    user_id = await database.execute(query)
    return {"id": user_id, **user.dict()}


async def get_user_private_info(user_id: int):
    """Gets user private info from database"""
    query = select(
        users.c.id,
        users.c.first_name,
        users.c.last_name,
        users.c.other_name,
        users.c.email,
        users.c.phone,
        users.c.birthday,
        users.c.city,
        users.c.additional_info,
        users.c.is_admin,
    ).where(users.c.id == user_id)
    res = await database.fetch_one(query)

    if res is None:
        raise HTTPException(
            status_code=404, detail=f"User with id: {user_id} not found"
        )

    return await database.fetch_one(query)


async def delete_user(user_id: int):
    """Tries to delete user from database"""
    await check_if_user_id_exists(user_id)

    await database.execute(delete(users).where(users.c.id == user_id))
    return {"msg": f"The user with id: {user_id} has been successfully deleted"}


async def change_current_user_info(user_id: str, new_info: BaseInfo):
    cur_email = await database.fetch_val(
        select(users.c.email).where(users.c.id == user_id)
    )
    if new_info.email != cur_email:
        await check_if_user_email_exists(new_info.email)

    query = (
        update(users)
        .where(users.c.id == user_id)
        .values(
            first_name=new_info.first_name,
            last_name=new_info.last_name,
            other_name=new_info.other_name,
            email=new_info.email,
            phone=new_info.phone,
            birthday=new_info.birthday,
        )
    )
    await database.execute(query)
    return {"id": user_id, **new_info.dict()}


async def change_user_info(user_id: int, new_info: PrivateUserModelInfo):
    """Changes user info in database"""
    await check_if_user_id_exists(user_id)
    await check_if_user_email_exists(new_info.email)

    query = (
        update(users)
        .where(users.c.id == user_id)
        .values(
            first_name=new_info.first_name,
            last_name=new_info.last_name,
            other_name=new_info.other_name,
            email=new_info.email,
            phone=new_info.phone,
            birthday=new_info.birthday,
            city=new_info.city,
            additional_info=new_info.additional_info,
            is_admin=new_info.is_admin,
        )
    )
    await database.execute(query)
    return {"id": user_id, **new_info.dict()}


async def get_user(email: str):
    """Gets user by email from database"""
    query = select(
        users.c.id,
        users.c.email,
        users.c.is_admin,
        users.c.password,
        users.c.first_name,
        users.c.last_name,
        users.c.other_name,
        users.c.phone,
        users.c.birthday,
    ).where(users.c.email == email)
    return await database.fetch_one(query)


async def get_short_user_info_paginate(params: Params):
    """Gets short users info from database with pagination"""
    query = select(users.c.id, users.c.first_name, users.c.last_name, users.c.email)
    return await paginate(database, query, params)


async def get_full_user_info_paginate(params: Params):
    """Gets full users info from database with pagination"""
    query = select(
        users.c.id,
        users.c.first_name,
        users.c.last_name,
        users.c.other_name,
        users.c.email,
        users.c.phone,
        users.c.birthday,
        users.c.city,
        users.c.additional_info,
        users.c.is_admin,
    )
    return await paginate(database, query, params)
