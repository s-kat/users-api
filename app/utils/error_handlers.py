from fastapi import HTTPException
from sqlalchemy import select

from app.models.database import database
from app.models.users import users


async def check_if_user_email_exists(email: str):
    if (
        await database.fetch_val(select(users.c.id).where(users.c.email == email))
        is not None
    ):
        raise HTTPException(
            status_code=422, detail=f"User with email: {email} already exists"
        )


async def check_if_user_id_exists(user_id: int):
    if (
        await database.fetch_val(select(users.c.id).where(users.c.id == user_id))
        is None
    ):
        raise HTTPException(
            status_code=404, detail=f"User with id: {user_id} not found"
        )
