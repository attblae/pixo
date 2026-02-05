from fastapi import FastAPI, HTTPException, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from schemes import RegisterIn, SignIn
from auth_service import login, save_user, users
from fastapi.exceptions import RequestValidationError
from create_tables import users_base
import sqlite3
import os
import uuid
from pathlib import Path


app = FastAPI()

UPLOAD_DIR = "static/works"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

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
            "message": 'Different problem',
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

@app.get("/account", tags=["lincs"])
def to_about():
    return FileResponse("pages/account.html")



@app.post("/login", tags=["user create/sign_in"])
def route_login(data: SignIn):
    return login(data)

@app.post("/registration", tags=["user create/sign_in"])
def register(data: RegisterIn):
    save_user(data)
    return {"status": "ok"}

@app.get("/users", tags=["user create/sign_in"])
def get_users():
    return users()



# Загрузка изображений
@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    results = []

    for file in files:
        try:
            # Проверяем расширение
            file_ext = Path(file.filename).suffix.lower()
            allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'}
            
            if file_ext not in allowed_extensions:
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "message": "Недопустимый формат"
                })
                continue
            
            # Читаем содержимое
            contents = await file.read()
            
            # Проверяем размер (10MB)
            if len(contents) > 10 * 1024 * 1024:
                results.append({
                    "filename": file.filename,
                    "status": "error", 
                    "message": "Файл слишком большой (макс. 10MB)"
                })
                continue
            
            # Генерируем уникальное имя
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = Path(UPLOAD_DIR) / unique_filename
            
            # Сохраняем файл
            with open(file_path, "wb") as f:
                f.write(contents)
            
            results.append({
                "filename": unique_filename,
                "original_filename": file.filename,
                "status": "success",
                "size": len(contents),
                "url": f"/static/works/{unique_filename}"  # URL для доступа
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": str(e)
            })
        finally:
            await file.close()
    
    return {"uploaded_files": results}

@app.get("/files")
def list_files():
    files = []
    upload_path = Path(UPLOAD_DIR)
    
    if upload_path.exists():
        for file_path in upload_path.iterdir():
            if file_path.is_file():
                files.append({
                    "filename": file_path.name,
                    "size": file_path.stat().st_size,
                    "url": f"/static/works/{file_path.name}"
                })
    
    return files

@app.get("/files/{filename}")
def get_file(filename: str):
    file_path = Path(UPLOAD_DIR) / filename
    
    if not file_path.exists() or not file_path.is_file():
        return JSONResponse(
            status_code=404,
            content={"detail": "Файл не найден"}
        )
    
    return FileResponse(file_path)



if __name__ == "__main__":
    import uvicorn
    # 127.0.0.1
    # 0.0.0.0
    con = sqlite3.connect("static/database.db")
    cursor = con.cursor()
    users_base(con, cursor)
    con.commit()
    con.close()
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8657,
        reload=True
    )