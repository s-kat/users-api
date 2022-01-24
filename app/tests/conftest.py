import os

import pytest

# Устанавливаем `os.environ`, чтобы использовать тестовую БД
os.environ['TESTING'] = 'True'

from alembic import command
from alembic.config import Config
from app.models import database
from sqlalchemy_utils import create_database, drop_database


@pytest.fixture(scope="module")
def temp_db():
    print("!!!!!!", database.TEST_SQLALCHEMY_DATABASE_URL)
    create_database('postgresql://postgres:postgres@localhost:7100/test')
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    print(alembic_cfg, flush=True)
    command.upgrade(alembic_cfg, "head")

    try:
        yield 'postgresql://postgres:postgres@localhost:7100/test'
    finally:
        pass
        drop_database('postgresql://postgres:postgres@localhost:7100/test')
