"""
This file defines the SQLAlchemy database models.
These classes are the Python representation of our database tables.
"""

from sqlalchemy import (Column, Integer, String, ForeignKey, Table)
from sqlalchemy.orm import relationship, declarative_base

dbBase = declarative_base()

# Association table for the many-to-many relationship
# between books and readers.
book_loans_table = Table(
    'book_loans',
    dbBase.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('reader_id', Integer, ForeignKey('readers.id', primary_key=True))
)


class Author(dbBase):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    # One-to-many relationship from Author to Book
    books = relationship("Book", back_populates="author")



class Book(dbBase):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))

    # Many-to-one link back Author
    author = relationship("Author", back_populates="books")

    # Many-to-many relationship to Readers
    readers = relationship("Reader",
        secondary = book_loans_table,
        back_populates = "read_books"
    )


class Reader(dbBase):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # Many-to-many link back to Books
    read_books = relationship("Book",
        secondary=book_loans_table,
        back_populates="readers"
    )