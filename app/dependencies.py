from fastapi import HTTPException, status
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from sqlmodel import select

from app.auth import JWT_ALGORITHM, JWT_SECRET_KEY, OAuth2Schema
from app.db.db import DbSession
from app.db.models.users import User


templates = Jinja2Templates(directory="app/templates")


def get_current_user(token: OAuth2Schema, session: DbSession) -> User:
    """Get the current user based on the provided OAuth2 token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user
