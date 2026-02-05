from fastapi import File, UploadFile
from fastapi.responses import JSONResponse

import os
import uuid
from pathlib import Path

# Правильный путь - от папки static где находятся py файлы до папки works
UPLOAD_DIR = "static/works"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def upload_images(files):
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
            
            # Проверяем размер (10MB)
            contents = file.read()
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
                "size": len(contents)
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": str(e)
            })
        finally:
            file.close()
    
    return {"uploaded_files": results}

def list_f():
    files = []
    upload_path = Path(UPLOAD_DIR)
    
    if upload_path.exists():
        for file_path in upload_path.iterdir():
            if file_path.is_file():
                files.append({
                    "filename": file_path.name,
                    "size": file_path.stat().st_size
                })
    
    return files

def geter_f(filename: str):
    file_path = Path(UPLOAD_DIR) / filename
    
    if not file_path.exists() or not file_path.is_file():
        return JSONResponse(
            status_code=404,
            content={"detail": "Файл не найден"}
        )
    
    from fastapi.responses import FileResponse
    return FileResponse(file_path)