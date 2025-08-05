from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.db.db import DbSession
from app.db.models.users import User

router = APIRouter()


@router.post("/create")
def create_user(user: User, session: DbSession):
    existing = session.exec(select(User).where(User.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/")
def list_users(session: DbSession):
    return session.exec(select(User)).all()
