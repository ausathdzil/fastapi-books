from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.models import Book, BookCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(engine)
