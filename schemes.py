from pydantic import BaseModel, Field

class SignIn(BaseModel):
    username: str
    password: str

class RegisterIn(BaseModel):
    username: str = Field(max_length=20)
    password: str = Field(min_length=6, max_length=20)
    password_conf: str = Field(min_length=6, max_length=20)
    name: str = Field(max_length=20)
    surname: str = Field(max_length=20)
    patronymic: str = Field(max_length=20)
    phone: str = Field(max_length=11)
    email: str = Field(min_length=12, max_length=30)
    passport_number: str = Field(min_length=6, max_length=15)
    card: str

# class Registration(RegisterIn):
#     name: str
#     surname: str
#     patronymic: str
#     phone: str
#     email: str
#     passport_series: str
#     passport_number: str
#     card: str


class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    email: str