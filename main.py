from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from schemes import RegisterIn, SignIn
from auth_service import login, save_user
from fastapi.exceptions import RequestValidationError


app = FastAPI()
app.mount("/static", StaticFiles(directory="static/"))

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "status_code": exc.status_code
        }
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


@app.get("/", tags=["lincs"])
def root():
    return FileResponse("pages/main.html")


@app.get("/sign", tags=["lincs"])
def to_sign():
    return FileResponse("pages/sign.html")

@app.get("/create", tags=["lincs"])
def to_create():
    return FileResponse("pages/create.html")

@app.get("/support", tags=["lincs"])
def to_support():
    return FileResponse("pages/support.html")

@app.get("/catalog", tags=["lincs"])
def to_catalog():
    return FileResponse("pages/catalog.html")

@app.get("/about_us", tags=["lincs"])
def to_about():
    return FileResponse("pages/about_us.html")

@app.post("/login")
def route_login(data: SignIn):
    return login(data)

@app.post("/registration")
def register(data: RegisterIn):
    save_user(data)
    return {"status": "ok"}

@app.get("/about_us", tags=["lincs"])
def get_db():



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