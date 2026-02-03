from fastapi import Depends, status
from fastapi import HTTPException
from schemes import TokenOut
from datetime import datetime, timedelta
from consts import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
import sqlite3

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(subject: str, expires_delta = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не авторизован",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise cred_exc
        return username
    except JWTError:
        raise cred_exc


def login(data):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()

    user = cursor.execute(
        "SELECT username, password FROM users WHERE ?",
        (data.username,)
    ).fetchone()
    cursor.close()
    print(user)

    # if not user:
    #     raise HTTPException(status_code=404, detail="User is not found")
    #
    # hash_pass = DB[data.username]['password']
    # if not verify_password(data.password, hash_pass):
    #     raise HTTPException(status_code=400, detail="Password does not valid")

    token = create_access_token(data.username)
    response = TokenOut(access_token=token)
    return response

def save_user(data):
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password is less then 6 symbols")
    if data.password != data.password_conf:
        raise HTTPException(status_code=400, detail="Password does not confirmed")

    import sqlite3
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    

    cursor.execute(
        """INSERT INTO users (
            username, 
            password, 
            name, 
            surname, 
            patronymic, 
            phone, 
            email, 
            passport_number, 
            card
            ) VAlUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.username,
            hash_password(data.password),
            data.name,
            data.surname,
            data.patronymic,
            data.phone,
            data.email,
            data.passport_number,
            data.card
        )
    )

    con.commit()