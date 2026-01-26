from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static/"))


# database = [
#     {
#         "id": 1,
#         "username": "test",
#         "age": 25
#     },
#     {
#         "id": 2,
#         "username": "tes2t",
#         "age": 22
#     }
# ]


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

@app.post('/pages')
def singin(data = Body()):
    username = data['username']
    password = data['password']



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