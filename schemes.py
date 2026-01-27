from pydantic import BaseModel

class SignIn(BaseModel):
    username: str
    password: str

class RegisterIn(BaseModel):
    username: str
    password: str
    password_conf: str

class Registration(RegisterIn):
    name: str
    surname: str
    patronymic: str
    phone: str
    email: str
    passport_series: str
    passport_number: str
    card: str


class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    email: str