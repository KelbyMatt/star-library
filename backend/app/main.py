from fastapi import FastAPI, Depends, HTTPException
from . import models, crud, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List


models.dbBase.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def main_library_root():
    return {"message": "STAR Library API"}

@app.post("/authors/", response_model=schemas.AuthorPublic)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=List[schemas.AuthorPublic])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.list_authors(db, skip=skip, limit=limit)
    return authors

@app.get("/authors/{author_id}", response_model=schemas.AuthorPublic)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=schemas.BookPublic)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=List[schemas.BookPublic])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.list_books(db, skip=skip, limit=limit)
    return books


@app.post("/readers/", response_model=schemas.ReaderPublic)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db)):
    return crud.create_reader(db=db, reader=reader)

@app.get("/readers/", response_model=List[schemas.ReaderPublic])
def read_readers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    readers = crud.list_readers(db, skip=skip, limit=limit)
    return readers