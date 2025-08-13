from datetime import date

from sqlmodel import Field, SQLModel


class BookBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    published_date: date | None = None
    summary: str | None = Field(default=None, max_length=1000)


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, min_length=1, max_length=255)
    published_date: date | None = Field(default=None)
    summary: str | None = Field(default=None, max_length=1000)


class BookPublic(BookBase):
    id: int


class BooksPublic(SQLModel):
    data: list[BookPublic]
    count: int
    page: int
    pages: int
    size: int
    has_next: bool
    has_prev: bool


class Message(SQLModel):
    message: str
