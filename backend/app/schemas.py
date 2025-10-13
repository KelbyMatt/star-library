"""
Pydantic models (schemas) for the API.
These define the shape of the data for requests and responses.
"""

from pydantic import BaseModel, ConfigDict
from typing import List


# --- Base Schemas ---

class BookBase(BaseModel):
    title: str

class AuthorBase(BaseModel):
    name: str

class ReaderBase(BaseModel):
    name: str


# --- Create Schemas ---

class BookCreate(BookBase):
    author_id: int

class AuthorCreate(AuthorBase):
    pass

class ReaderCreate(ReaderBase):
    pass


# --- Public Schemas ---

# The "In" schemas are the key to preventing an infinite loop from the
# circular dependency between the Author and Book models.
class BookInAuthor(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class AuthorInBook(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)



class BookPublic(BookBase):
    id: int
    author: AuthorInBook
    model_config = ConfigDict(from_attributes=True)

class AuthorPublic(AuthorBase):
    id: int
    books: List[BookInAuthor] = []
    model_config = ConfigDict(from_attributes=True)

class ReaderPublic(ReaderBase):
    id: int
    read_books: List[BookPublic] = []
    model_config = ConfigDict(from_attributes=True)