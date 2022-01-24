from datetime import datetime

from pydantic import BaseModel, EmailStr, validator


class BaseInfo(BaseModel):
    first_name: str
    last_name: str
    other_name: str
    email: EmailStr
    phone: str
    birthday: str

    @validator("birthday")
    def birthday_validation(cls, birthday):
        datetime.strptime(birthday, "%d-%m-%Y")
        return birthday


class PrivateCreateUserModel(BaseInfo):
    additional_info: str
    city: int
    password: str
    is_admin: bool


class PrivateChangeUserInfo(BaseInfo):
    additional_info: str
    city: int
    is_admin: bool


class PrivateUserModelInfo(BaseInfo):
    id: int
    additional_info: str
    city: int
    is_admin: bool


class ChangedBaseUserInfo(BaseInfo):
    id: int


class LoginModel(BaseModel):
    login: str
    password: str


class ShortUserInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
