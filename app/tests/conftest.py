import os
from os import environ

import pytest

# Устанавливаем `os.environ`, чтобы использовать тестовую БД
os.environ["TESTING"] = "True"
os.environ["DB_NAME"] = "test"
DB_USER = environ.get("DB_USER", "postgres")
DB_PASSWORD = environ.get("DB_PASSWORD", "postgres")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_NAME = environ.get("DB_NAME", "postgres")

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy_utils import create_database, drop_database

from app.main import app
from app.schemas.users import PrivateCreateUserModel
from app.tests.utils import login_admin_user


@pytest.fixture(scope="module")
def temp_db():
    create_database(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    command.upgrade(alembic_cfg, "head")

    try:
        yield f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    finally:
        pass
        drop_database(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}")


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
