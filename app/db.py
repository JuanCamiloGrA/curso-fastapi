from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"


engine = create_engine(sqlite_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
def create_db_and_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


SessionDep = Annotated[Session, Depends(get_session)]
