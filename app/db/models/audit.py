from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel

from app.db.models.users import User


class AuditTrail(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    action: str  # e.g., "CREATE_PRODUCT", "UPDATE_STOCK", "DELETE_BRANCH"
    model: str  # e.g., "Product", "Inventory"
    model_id: int | None = None
    description: str | None = None
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))

    user: User | None = Relationship()
