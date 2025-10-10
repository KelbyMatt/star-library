from pydantic import BaseModel, ConfigDict
from typing import List

class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass


class AuthorPublic(AuthorBase):
    id: int
    books: List['BookPublic'] = []

    model_config = ConfigDict(from_attributes=True)

class BookBase(BaseModel):
    title: str

class BookCreate(BookBase):
    author_id: int

class BookPublic(BookBase):
    id: int
    author: Author

    model_config = ConfigDict(from_attributes=True)

class ReaderBase(BaseModel):
    name: str

class ReaderCreate(ReaderBase):
    pass

class ReaderPublic(ReaderBase):
    id: int
    read_books: List[Book] = []

    model_config = ConfigDict(from_attributes=True)

AuthorPublic.model_rebuild()