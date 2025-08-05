from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel
from app.conf import settings

engine = create_engine(settings.database_url)


def create_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session


DbSession = Annotated[Session, Depends(get_session)]
