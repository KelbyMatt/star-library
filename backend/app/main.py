from fastapi import FastAPI
from . import models
from .database import engine

models.dbBase.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def main_library_root():
    return {"message": "STAR Library API"}