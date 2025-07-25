from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel

engine = create_engine("file://db.sqlite3")


def create_db():
    SQLModel.metadata.create_all(engine)


def get_sesion() -> Generator[Session]:
    with Session(engine) as session:
        yield session


DbSession = Annotated[Session, Depends(get_sesion)]
