from sqlmodel import SQLModel, Field, Relationship


class Role(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    users: list["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str
    email: str | None = Field(default=None, unique=True)
    is_active: bool = Field(default=True)
    role_id: int = Field(foreign_key="role.id")

    role: Role = Relationship(back_populates="users")
