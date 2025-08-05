from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from app.db.db import DbSession
from app.db.models.users import User
from app.auth import verify_password, get_password_hash, create_access_token

router = APIRouter()


@router.post("/register")
def register_user(user: User, session: DbSession):
    existing_user = session.exec(
        select(User).where(User.username == user.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user.password_hash = get_password_hash(user.password_hash)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User registered"}


@router.post("/login")
def login(session: DbSession, payload: OAuth2PasswordRequestForm = Depends()):
    user = session.exec(select(User).where(User.username == payload.username)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
