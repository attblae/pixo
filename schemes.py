from pydantic import BaseModel

class RegisterIn(BaseModel):
    username: str
    password: str

class Registration(BaseModel):
    name: str
    surname: str
    patronymic: str
    phone: str
    email: str
    passport_series: str
    passport_number: str
    card: str
    username: str
    password: str


class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    email: str