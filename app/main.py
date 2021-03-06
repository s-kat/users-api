from os import environ

import uvicorn
from fastapi import FastAPI
from sqlalchemy import select

from app.models.database import database
from app.models.users import users
from app.routers import admin, login, pagintaion, user
from app.schemas.users import PrivateCreateUserModel

app = FastAPI()
from werkzeug.security import generate_password_hash

ADMIN_USER = environ.get("ADMIN_USER", "admin@gmail.com")
ADMIN_PASSWORD = environ.get("ADMIN_PASSWORD", "0000")


@app.on_event("startup")
async def startup():
    await database.connect()

    # init admin user
    user = PrivateCreateUserModel(
        first_name="admin",
        last_name="admin",
        other_name="admin",
        email=ADMIN_USER,
        phone="132342341",
        birthday="01-01-2000",
        additional_info="",
        password=ADMIN_PASSWORD,
        city=0,
        is_admin=True,
    )
    if (
        await database.fetch_val(
            select(users.c.id).where(users.c.email == "admin@gmail.com")
        )
        is None
    ):
        hashed_password = generate_password_hash(user.password)
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
        await database.execute(query)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(admin.router)
app.include_router(login.router)
app.include_router(user.router)
app.include_router(pagintaion.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
