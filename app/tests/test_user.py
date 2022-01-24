from fastapi.testclient import TestClient

from app.main import app
from app.schemas.users import BaseInfo
from app.tests.models import new_user_model
from app.tests.utils import create_test_user, delete_test_user, login_user


def test_private_routes(temp_db):
    new_user = create_test_user(new_user_model)
    user_cookie = login_user({"login": "test@mail.ru", "password": "test"})
    with TestClient(app) as client:
        response = client.delete(f"/private/users/1111", cookies=user_cookie)
        assert response.status_code == 401

        response = client.get(f"/private/users/{new_user['id']}", cookies=user_cookie)
        assert response.status_code == 401

    delete_test_user(new_user["id"])


def test_get_current_info(temp_db):
    new_user = create_test_user(new_user_model)
    user_cookie = login_user(
        {"login": new_user_model["email"], "password": new_user_model["password"]}
    )

    with TestClient(app) as client:
        response = client.get(f"/users/current", cookies=user_cookie)

        assert response.status_code == 200
        assert response.json()["email"] == new_user["email"]
        assert response.json()["first_name"] == new_user["first_name"]
        assert response.json()["phone"] == new_user["phone"]
        assert response.json()["birthday"] == new_user["birthday"]

    delete_test_user(new_user["id"])


def update_current_user_info(temp_db):
    new_user = create_test_user(new_user_model)
    user_cookie = login_user(
        {"login": new_user_model["email"], "password": new_user_model["password"]}
    )

    with TestClient(app) as client:
        new_info = BaseInfo(
            first_name="new-name",
            last_name="new-name",
            other_name="new-name",
            email="aa@mail.ru",
            phone="123423",
            birthday="02-02-1023",
        ).dict()

        response = client.patch("/users", json=new_info, cookies=user_cookie)

        assert response.status_code == 200
        assert response.json()["first_name"] == new_info["first_name"]
        assert response.json()["email"] == new_info["email"]

        new_user_cookie = login_user(
            {"login": new_info["email"], "password": new_user_model["password"]}
        )

        response = client.get(f"/users/current", cookies=new_user_cookie)

        assert response.status_code == 200
        assert response.json()["email"] == new_info["email"]
        assert response.json()["first_name"] == new_info["first_name"]
        assert response.json()["phone"] == new_info["phone"]
        assert response.json()["birthday"] == new_info["birthday"]

    delete_test_user(new_user["id"])
