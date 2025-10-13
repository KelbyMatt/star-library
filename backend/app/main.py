"""
Main API file for STAR Library.
This contains all the public-facing endpoints for the application.
"""

from fastapi import FastAPI, Depends, HTTPException
from . import models, crud, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import  desc, func
from typing import List, Optional
from collections import Counter


app = FastAPI()

"""This function makes sure we get a database session for each request
and that it's always closed when the request is done."""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api")
def main_library_root():
    return {
            "api_name": "STAR Library API",
            "version": "0.1-dev",
            "status": "ok"
            }


# --- Basic CRUD Endpoints ---

@app.post("/api/authors/", response_model=schemas.AuthorPublic)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """Endpoint to create a new author."""
    return crud.create_author(db=db, author=author)

@app.get("/api/authors/", response_model=List[schemas.AuthorPublic])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Endpoint to get a list of all authors."""
    authors = crud.list_authors(db, skip=skip, limit=limit)
    return authors

@app.get("/api/authors/{author_id}", response_model=schemas.AuthorPublic)
def read_author(author_id: int, db: Session = Depends(get_db)):
    """Endpoint to get a single author by their ID."""
    db_author = crud.get_author_by_id(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/api/books/", response_model=schemas.BookPublic)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

@app.get("/api/books/", response_model=List[schemas.BookPublic])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.list_books(db, skip=skip, limit=limit)
    return books


@app.post("/api/readers/", response_model=schemas.ReaderPublic)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db)):
    return crud.create_reader(db=db, reader=reader)

@app.get("/api/readers/", response_model=List[schemas.ReaderPublic])
def read_readers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    readers = crud.list_readers(db, skip=skip, limit=limit)
    return readers


# --- Custom Statistical Endpoints ---

@app.get("/api/books/popular", response_model=List[schemas.BookPublic])
def get_popular_books(db: Session = Depends(get_db)):
    # Join books with the loans table, group by book, and count the readers.
    popular_books = (
        db.query(models.Book)
        .join(models.book_loans_table)
        .group_by(models.Book.id)
        .order_by(desc(func.count(models.book_loans_table.c.reader_id)))
        .limit(10)
        .all()
    )
    return popular_books

def _get_user_top_authors(user: models.Reader,limit: int = 3) -> List[models.Author]:
    """
    Helper to figure out a users favorite authors.
    Just counts the books read for each author and returns the top ones.
    I pulled this out to keep the main dashboard endpoint clean.
    """
    if not user.read_books:
        return []
    
    # Tallying up authors via Counter.
    authors_books_read_count = Counter(book.author for book in user.read_books)
    top_authors_with_counts = authors_books_read_count.most_common(limit)

    top_authors = [author for author, count in top_authors_with_counts]
    return top_authors


@app.get("/api/dashboard/stats")
def get_reader_dashboard(db: Session = Depends(get_db)):
    """The main endpoint for the frontend dashboard, providing all key stats."""

    # Only due to Assessment requirement, assuming we are logged in as said user.
    SIGNED_IN_READER_ID = 1

    # Finds the author with the highest total book readership across the whole library.
    most_popular_author_query = (
        db.query(models.Author, func.count(models.book_loans_table.c.reader_id).label("read_count"))
        .select_from(models.Author) 
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