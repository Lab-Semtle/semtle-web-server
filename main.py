from fastapi import FastAPI

from src.var import models
from src.var.session import engine
models.Base.metadata.create_all(bind=engine)

from src.api.v1.post import post_control

app = FastAPI()

app.include_router(post_control.app, tags = ["board"])

@app.get("/")
def read_root():
    return {    
        "project": "Arch Sebtle Web DEV",
        "name": "게시판 API",
        "github repo": "https://github.com/Lab-Semtle/Semtle-Web-Server",
        "version": "0.0.1"
    }