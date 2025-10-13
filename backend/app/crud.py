"""
This file holds all the reusable functions for interacting
with the database. Separates DB logic from API endpoint logic.
"""

from sqlalchemy.orm import Session
from . import models, schemas


# --- Author Functions ---

def get_author_by_id(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_author_by_name(db: Session, name: str): 
    return db.query(models.Author).filter(models.Author.name == name).first()

def list_authors(db: Session, skip: int = 0, limit: int = 100):
    """Gets a paginated list of all authors."""    
    return db.query(models.Author).offset(skip).limit(limit).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    """
    If an author with the same name already exists, it returns the
    existing author instead of duplicating.
    """
    existing_author = get_author_by_name(db, name=author.name) 
    if existing_author:
        return existing_author
        
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


# --- Book Functions ---

def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def list_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    """Note: Scalability in mind, do not have duplicates accounted for,
    common to have books with same names but different volumes, editions, etc."""
    db_book = models.Book(title=book.title, author_id=book.author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# --- Reader Functions ---

def get_reader_by_id(db: Session, reader_id: int):
    return db.query(models.Reader).filter(models.Reader.id == reader_id).first()

def get_reader_by_name(db: Session, name: str): 
    return db.query(models.Reader).filter(models.Reader.name == name).first()

def list_readers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Reader).offset(skip).limit(limit).all()

def create_reader(db: Session, reader: schemas.ReaderCreate):
    existing_reader = get_reader_by_name(db, name=reader.name)
    if existing_reader:
        return existing_reader

    db_reader = models.Reader(name=reader.name)
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader