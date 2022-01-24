import sqlalchemy

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("other_name", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("phone", sqlalchemy.String),
    sqlalchemy.Column("birthday", sqlalchemy.String),
    sqlalchemy.Column("city", sqlalchemy.Integer),
    sqlalchemy.Column("additional_info", sqlalchemy.String),
    sqlalchemy.Column("is_admin", sqlalchemy.Boolean),
    sqlalchemy.Column("password", sqlalchemy.String),
)
