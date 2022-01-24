import os

import pytest

# Устанавливаем `os.environ`, чтобы использовать тестовую БД
os.environ["TESTING"] = "True"

import asyncio

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy_utils import create_database, drop_database

from app.main import app
from app.models import database
from app.schemas.users import LoginModel, PrivateCreateUserModel
from app.tests.utils import login_admin_user


@pytest.fixture(scope="module")
def temp_db():
    create_database("postgresql://postgres:postgres@localhost:7100/test")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    command.upgrade(alembic_cfg, "head")

    try:
        yield "postgresql://postgres:postgres@localhost:7100/test"
    finally:
        pass
        drop_database("postgresql://postgres:postgres@localhost:7100/test")


@pytest.fixture(scope="function")
def admin_login_cookies():
    yield login_admin_user()


@pytest.fixture(scope="function")
def test_user(temp_db):
    admin_user = {"login": "admin@gmail.com", "password": "0000"}
    with TestClient(app) as client:
        # Create user and use his token to add new post
        response = client.post(
            "/login",
            json=admin_user,
        )
        assert response.status_code == 200

    admin_login_cookies = response.cookies

    new_user = PrivateCreateUserModel(
        first_name="test",
        last_name="test",
        other_name="test",
        email="test@mail.ru",
        phone="1111111",
        birthday="01-01-2000",
        additional_info="",
        city=1,
        password="1234",
        is_admin=False,
    ).dict()

    with TestClient(app) as client:
        # create new user
        response = client.post(
            "/private/users", json=new_user, cookies=admin_login_cookies
        )

    yield response.json()

    # delete test user
    response = client.delete(
        f"/private/users/{response.json()['id']}", cookies=admin_login_cookies
    )
