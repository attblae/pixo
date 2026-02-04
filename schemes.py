from pydantic import BaseModel, Field

class SignIn(BaseModel):
    username: str = Field(min_length=2, max_length=30)
    password: str = Field(min_length=6, max_length=35)

class RegisterIn(BaseModel):
    username: str = Field(min_length=2, max_length=30)
    password: str = Field(min_length=6, max_length=35)
    password_conf: str
    name: str = Field(min_length=2, max_length=30)
    surname: str = Field(min_length=4, max_length=30)
    patronymic: str = Field(min_length=4, max_length=30)
    phone: str = Field(min_length=11, max_length=11)
    email: str = Field(min_length=10, max_length=45)
    passport_number: str = Field(min_length=6, max_length=15)
    card: str = Field(min_length=16, max_length=30)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    email: str