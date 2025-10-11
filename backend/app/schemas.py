from pydantic import BaseModel, ConfigDict
from typing import List


class BookBase(BaseModel):
    title: str

class AuthorBase(BaseModel):
    name: str

class ReaderBase(BaseModel):
    name: str


class BookCreate(BookBase):
    author_id: int

class AuthorCreate(AuthorBase):
    pass

class ReaderCreate(ReaderBase):
    pass


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
  
    read_books: List[BookPublic] = []
    model_config = ConfigDict(from_attributes=True)