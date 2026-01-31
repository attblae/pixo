from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from schemes import RegisterIn, SignIn, TokenOut
from utils import hash_password, verify_password, create_access_token
from fastapi.exceptions import RequestValidationError


app = FastAPI()

app.mount("/static", StaticFiles(directory="static/"))

DB = {'attblae': {
        'password': '$pbkdf2-sha256$29000$S4kRIoTQ2ts757yX0ppTCg$wIXLTvKHpqWpurOiuvImHQInJpDeQh0JBgqC774WX68',
        'name': 'N',
        'surname': 'G',
        'patronymic': 'S',
        'phone': '9155554455',
        'email': 'gns@gmail.com',
        'passport_number': '1234',
        'card': '123456789'
    }
}


@app.get("/", tags=["lincs"])
def root():
    return FileResponse("pages/main.html")


@app.get("/sign", tags=["lincs"])
def to_sign():
    return FileResponse("pages/sign.html")

@app.get("/catalog", tags=["lincs"])
def to_catalog():
    return FileResponse("pages/catalog.html")

@app.get("/about_us", tags=["lincs"])
def to_about():
    return FileResponse("pages/about_us.html")

@app.get("/create_id", tags=["lincs"])
def to_createid():
    return FileResponse("pages/create_id.html")

@app.get("/create", tags=["lincs"])
def to_create():
    return FileResponse("pages/create.html")

@app.get("/support", tags=["lincs"])
def to_support():
    return FileResponse("pages/support.html")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "status_code": exc.status_code
        },
        headers=exc.headers
    )


# Обработка ошибок валидации
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "message": 'exc.detail',
            "errors": exc.errors(),
            "body": exc.body
        }
    )

# ===== ПОСТЫ =====
@app.post("/login")
def login(data: SignIn):
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password is less then 6 symbols")

    if not DB.get(data.username):
        raise HTTPException(status_code=404, detail="User is not found")

    hash_pass = DB[data.username]['password']
    if not verify_password(data.password, hash_pass):
        raise HTTPException(status_code=400, detail="Password does not valid")

    token = create_access_token(data.username)
    response = TokenOut(access_token=token)
    return response

@app.post("/registration")
def register(data: RegisterIn):
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password is less then 6 symbols")
    if data.password != data.password_conf:
        raise HTTPException(status_code=400, detail="Password does not confirmed")

    DB[data.username] = {
        "password": hash_password(data.password),
        "name": data.name,
        "surname": data.surname,
        "patronymic": data.patronymic,
        "phone": data.phone,
        "email": data.email,
        "passport_number": data.passport_number,
        "card": data.card
    }
    print(DB[data.username])

    return {"status": "ok"}

@app.get("/users")
def get_users():
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