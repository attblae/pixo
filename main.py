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

@app.post('/pages'):
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