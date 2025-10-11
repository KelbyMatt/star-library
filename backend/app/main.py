from fastapi import FastAPI, Depends, HTTPException
from . import models, crud, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import  desc, func
from typing import List, Optional
from collections import Counter

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


@app.get("/books/popular", response_model=List[schemas.BookPublic])
def get_popular_books(db: Session = Depends(get_db)):
    popular_books = (
        db.query(models.Book)
        .join(models.book_loans_table)
        .group_by(models.Book.id)
        .order_by(desc(func.count(models.book_loans_table.c.reader_id)))
        .all()
    )
    return popular_books

def _get_user_top_authors(user: models.Reader,limit: int = 3) -> List[models.Author]:
    if not user.read_books:
        return []
    
    authors_books_read_count = Counter(book.author for book in user.read_books)
    top_authors_with_counts = authors_books_read_count.most_common(limit)

    top_authors = [author for author, count in top_authors_with_counts]
    return top_authors


@app.get("/dashboard/stats")
def get_reader_dashboard(db: Session = Depends(get_db)):

    SIGNED_IN_READER_ID = 1

    most_popular_author_query = (
        db.query(models.Author, func.count(models.book_loans_table.c.reader_id).label("read_count"))
        .join(models.Book)
        .join(models.book_loans_table)
        .group_by(models.Author)
        .order_by(desc("read_count"))
        .first()
    )
    most_popular_author = most_popular_author_query[0] if most_popular_author_query else None

    active_reader = crud.get_reader_by_id(db, reader_id=SIGNED_IN_READER_ID)
    if not active_reader:
        raise HTTPException(
            status_code=404, 
            detail=f"The active reader (ID: {SIGNED_IN_READER_ID}) could not be found."
        )

    total_books_read = len(active_reader.read_books)
    favorite_authors = _get_user_top_authors(active_reader, limit=3)

    return {
        "library_wide_stats": {
            "most_popular_author": schemas.AuthorPublic.model_validate(most_popular_author) if most_popular_author else None,
        },
        "personal_stats": {
            "user_profile": schemas.ReaderPublic.model_validate(active_reader),
            "total_books_read": total_books_read,
            "favorite_authors": [schemas.AuthorPublic.model_validate(author) for author in favorite_authors],
        }
    }