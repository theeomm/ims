from collections.abc import Generator
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import create_engine, Session, SQLModel
from app.conf import settings

engine = create_engine(settings.database_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db
    yield


def create_db():
    SQLModel.metadata.create_all(engine)


def get_sesion() -> Generator[Session]:
    with Session(engine) as session:
        yield session


DbSession = Annotated[Session, Depends(get_sesion)]
