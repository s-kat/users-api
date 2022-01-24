from fastapi.testclient import TestClient

from app.main import app
from app.schemas.users import PrivateChangeUserInfo
from app.tests.models import new_user_model
from app.tests.utils import create_test_user, delete_test_user


def test_login(temp_db):
    admin_user = {"login": "admin@gmail.com", "password": "0000"}
    fake_user = {"login": "admin@gmail.com", "password": "1234"}
    fake_user1 = {"login": "test@gmail.com", "password": "1111"}
    with TestClient(app) as client:
        response = client.post(
            "/login",
            json=admin_user,
        )
        assert response.status_code == 200

        response = client.post(
            "/login",
            json=fake_user,
        )
        assert response.status_code == 401
        response = client.post(
            "/login",
            json=fake_user1,
        )
        assert response.status_code == 401


def test_create_user(admin_login_cookies):

    new_user = create_test_user(new_user_model)
    with TestClient(app) as client:
        # try to create existent user
        response = client.post(
            "/private/users", json=new_user, cookies=admin_login_cookies
        )
        assert response.status_code == 422
    delete_test_user(new_user["id"])


def test_get_user_info(temp_db, admin_login_cookies):
    test_user = create_test_user(new_user_model)

    with TestClient(app) as client:
        response = client.get(
            f"/private/users/{test_user['id']}", cookies=admin_login_cookies
        )
        assert response.status_code == 200
        assert response.json()["first_name"] == "test"
        assert response.json()["email"] == "test@mail.ru"

        response = client.get(f"/private/users/111", cookies=admin_login_cookies)
        assert response.status_code == 404
    delete_test_user(test_user["id"])


def test_delete_user(temp_db, admin_login_cookies):
    test_user = create_test_user(new_user_model)

    with TestClient(app) as client:
        response = client.delete(
            f"/private/users/{test_user['id']}", cookies=admin_login_cookies
        )
        assert response.status_code == 204

        # try to get
        response = client.get(
            f"/private/users/{test_user['id']}", cookies=admin_login_cookies
        )
        assert response.status_code == 404

        # try to delete non-existent user
        response = client.delete(f"/private/users/111", cookies=admin_login_cookies)
        assert response.status_code == 404


def test_change_private_user_info(temp_db, admin_login_cookies):
    test_user = create_test_user(new_user_model)

    with TestClient(app) as client:
        change_good = PrivateChangeUserInfo(
            first_name="test1",
            last_name="test1",
            other_name="test1",
            email="ttt@mail.ru",
            phone="242342",
            birthday="01-01-1999",
            additional_info="",
            city=1,
            is_admin=False,
        )
        response = client.patch(
            f"/private/users/{test_user['id']}",
            json=change_good.dict(),
            cookies=admin_login_cookies,
        )

        assert response.status_code == 200
        assert response.json()["first_name"] == "test1"
        assert response.json()["email"] == "ttt@mail.ru"
        assert response.json()["phone"] == "242342"

        # try to set existing email
        change_exist_email = PrivateChangeUserInfo(
            first_name="test1",
            last_name="test1",
            other_name="test1",
            email="admin@gmail.com",
            phone="242342",
            birthday="01-01-1999",
            additional_info="",
            city=1,
            is_admin=False,
        )
        response = client.patch(
            f"/private/users/{test_user['id']}",
            json=change_exist_email.dict(),
            cookies=admin_login_cookies,
        )
        assert response.status_code == 422
    delete_test_user(test_user["id"])
