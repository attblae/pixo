from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from schemes import RegisterIn
from utils import hash_password


app = FastAPI()

app.mount("/static", StaticFiles(directory="static/"))

DB = {}


@app.get("/")
def root():
    return FileResponse("pages/main.html")


@app.get("/sign")
def root():
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
@app.post("/register")
def register(data: RegisterIn):
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Пароль минимум 6 символов")

    DB[data.username] = hash_password(data.password)

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