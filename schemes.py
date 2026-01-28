from pydantic import BaseModel, Field

class SignIn(BaseModel):
    username: str
    password: str

class RegisterIn(BaseModel):
    username: str = Field(min_length=2, max_length=20)
    password: str = Field(min_length=6, max_length=20)
    password_conf: str = Field(min_length=6, max_length=20)
    name: str = Field(min_length=2, max_length=20)
    surname: str = Field(min_length=2, max_length=20)
    patronymic: str = Field(min_length=2, max_length=20)
    phone: str = Field(min_length=11, max_length=11)
    email: str = Field(min_length=12, max_length=30)
    passport_number: str = Field(min_length=6, max_length=15)
    card: str = Field(min_length=16, max_length=16)

class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    email: str