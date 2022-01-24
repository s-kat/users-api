from app.schemas.users import LoginModel, PrivateCreateUserModel

new_user_model = PrivateCreateUserModel(
    first_name="test",
    last_name="test",
    other_name="test",
    email="test@mail.ru",
    phone="1111111",
    birthday="01-01-2000",
    additional_info="",
    city=1,
    password="test",
    is_admin=False,
).dict()
