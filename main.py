from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from schemes import RegisterIn, Registration, SignIn
from utils import hash_password


app = FastAPI()

app.mount("/static", StaticFiles(directory="static/"))

DB = {"dfhgkdfg": {'dfkjds': "sdljfhskd"}}


@app.get("/")
def root():
    return FileResponse("pages/main.html")


@app.get("/sign")
def to_sign():
    return FileResponse("pages/sign.html")

@app.get("/catalog")
def to_catalog():
    return FileResponse("pages/catalog.html")

@app.get("/about_us")
def to_about():
    return FileResponse("pages/about_us.html")

@app.get("/create_id")
def to_createid():
    return FileResponse("pages/create_id.html")

@app.get("/create")
def to_create():
    return FileResponse("pages/create.html")

@app.get("/support")
def to_support():
    return FileResponse("pages/support.html")

# ===== ПОСТЫ =====
@app.post("/login")
def login(data: SignIn,):
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password is less then 6 symbols")
    if data.username in DB.keys():
        return {"status": "ok"}

# @app.post("/registrate")
# def register(data: RegisterIn):
#     if data.password is None or data.username is None:
#         raise HTTPException(status_code=400, detail="Field is empty")
#     if len(data.password) < 6:
#         raise HTTPException(status_code=400, detail="Password is less then 6 symbols")
#     if data.password != data.password_conf:
#         raise HTTPException(status_code=400, detail="Password does not confirmed")
#
#     return {"status": "ok"}

@app.post("/registration")
def register(data: RegisterIn):
    if data.password is None or data.username is None:
        raise HTTPException(status_code=400, detail="Field is empty")
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
        "passport_series": data.passport_series,
        "passport_number": data.passport_number,
        "card": data.card
    }

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