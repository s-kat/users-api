from fastapi.testclient import TestClient

from app.main import app


def login_user(user_login_model):
    with TestClient(app) as client:
        response = client.post(
            "/login",
            json=user_login_model,
        )
        assert response.status_code == 200
    return response.cookies


def login_admin_user():
    admin_user = {"login": "admin@gmail.com", "password": "0000"}
    return login_user(admin_user)


def create_test_user(new_user):
    cookies = login_admin_user()

    with TestClient(app) as client:
        # create new user
        response = client.post("/private/users", json=new_user, cookies=cookies)
        assert response.status_code == 201
    return response.json()


def delete_test_user(user_id):
    cookies = login_admin_user()
    # delete test user
    with TestClient(app) as client:
        response = client.delete(f"/private/users/{user_id}", cookies=cookies)
        assert response.status_code == 204
