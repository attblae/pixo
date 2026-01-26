from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
app = FastAPI()

app.mount("/static", StaticFiles(directory="static/"))


SECRET_KEY = "change-me-in-production-please"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DB = {}


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# ===== КЛАССЫ =====
class RegisterIn(BaseModel):
    username: str
    password: str


class LoginIn(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    email: str


# ===== НАДО =====
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(subject: str, expires_delta = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_email(token: str = Depends(oauth2_scheme)) -> str:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не авторизован",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise cred_exc
        return email
    except JWTError:
        raise cred_exc


def normalize_email(email: str) -> str:
    return email.strip().lower()


def validate_email(email: str) -> None:
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Некорректная почта")

@app.get("/")
def root():
    return FileResponse("pages/main.html")


@app.get("/sign")
def root():
    return FileResponse("pages/sign.html")

@app.get("/catalog")
def root():
    return FileResponse("pages/catalog.html")

@app.get("/about_us")
def root():
    return FileResponse("pages/about_us.html")

@app.get("/create_id")
def root():
    return FileResponse("pages/create_id.html")

@app.get("/create")
def root():
    return FileResponse("pages/create.html")

@app.get("/support")
def root():
    return FileResponse("pages/support.html")

# ===== ПОСТЫ =====
@app.post("/register")
def reg(data: RegisterIn):
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Пароль минимум 6 символов")

    DB[data.username] = hash_password(data.password)

    return {"status": "ok"}


@app.get("/users")
def register():
    return DB



if __name__ == "__main__":
    import uvicorn
    # 127.0.0.1
    # 0.0.0.0
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8657,
        reload=True
    )