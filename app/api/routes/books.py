from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, or_, select

from app.api.deps import SessionDep
from app.models import Book, BookCreate, BookPublic, BooksPublic, BookUpdate, Message

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=BooksPublic)
def read_books(
    session: SessionDep, q: str | None = None, page: int = 1, size: int = 10
) -> Any:
    """
    Retrieve books with pagination.
    """
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    if size > 20:
        size = 20

    skip = (page - 1) * size

    base_statement = select(Book)
    if q:
        search_filter = or_(
            Book.title.ilike(f"%{q}%"),
            Book.author.ilike(f"%{q}%"),
        )
        base_statement = base_statement.where(search_filter)

    count_statement = select(func.count()).select_from(base_statement.subquery())
    count = session.exec(count_statement).one()

    pages = (count + size - 1) // size
    has_next = page < pages
    has_prev = page > 1

    statement = base_statement.offset(skip).limit(size)
    books = session.exec(statement).all()

    return BooksPublic(
        data=books,
        count=count,
        page=page,
        pages=pages,
        size=size,
        has_next=has_next,
        has_prev=has_prev,
    )


@router.get("/{id}", response_model=BookPublic)
def read_book(session: SessionDep, id: int) -> Any:
    """
    Get book by ID.
    """
    book = session.get(Book, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=BookPublic)
def create_book(session: SessionDep, book_in: BookCreate) -> Any:
    """
    Create a new book.
    """
    book = Book.model_validate(book_in)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.put("/{id}", response_model=BookPublic)
def update_book(session: SessionDep, id: int, book_in: BookUpdate) -> Any:
    """
    Update a book.
    """
    book = session.get(Book, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    update_dict = book_in.model_dump(exclude_unset=True)
    book.sqlmodel_update(update_dict)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.delete("/{id}", response_model=Message)
def delete_book(session: SessionDep, id: int) -> Any:
    """
    Delete a book.
    """
    book = session.get(Book, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return Message(message="Book deleted successfully")
