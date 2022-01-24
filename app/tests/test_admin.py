import asyncio
from re import U

from app.main import app
from fastapi.testclient import TestClient
from app.schemas.users import LoginModel

def test_login(temp_db):
    admin_user = {
      "login": "admin@gmail.com",
      "password": "0000"
    }
    fake_user = {
        "login": "admin@gmail.com",
        "password": "1234"
    }
    fake_user1 = {
        "login": "test@gmail.com",
        "password": "1111"
    }
    with TestClient(app) as client:
        return
        # Create user and use his token to add new post
        response = client.post(
            "/posts",
            json=admin_user,
        )
        assert response.status_code == 201
        assert response.json()["id"] == 1
        assert response.json()["title"] == "42"
        assert response.json()["content"] == "Don't panic!"
