from os import environ

import databases

DB_USER = environ.get("DB_USER", "postgres")
DB_PASSWORD = environ.get("DB_PASSWORD", "postgres")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_NAME = "db"

TESTING = environ.get("TESTING")

if TESTING:
    # Use separate DB for tests
    DB_NAME = "test"
    TEST_SQLALCHEMY_DATABASE_URL = (
        f"postgresql://postgres:postgres@localhost:7100/test"
    )
    database = databases.Database(TEST_SQLALCHEMY_DATABASE_URL)
else:
    SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@localhost:7100/postgres"
    database = databases.Database(SQLALCHEMY_DATABASE_URL)
