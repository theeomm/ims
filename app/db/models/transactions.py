from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel

# from app.db.models.inventory import Branch, Product, Supplier
from app.db.models.users import User


class Sale(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    branch_id: int = Field(foreign_key="branch.id")
    user_id: int | None = Field(default=None, foreign_key="user.id")
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    total_amount: float

    branch: "Branch" = Relationship(back_populates="sales")
    items: list["SaleItem"] = Relationship(back_populates="sale")
    user: User | None = Relationship()


class SaleItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sale_id: int = Field(foreign_key="sale.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    unit_price: float

    sale: Sale = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="sale_items")


class Purchase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    branch_id: int = Field(foreign_key="branch.id")
    supplier_id: int = Field(foreign_key="supplier.id")
    user_id: int | None = Field(default=None, foreign_key="user.id")
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    total_cost: float

    branch: "Branch" = Relationship(back_populates="purchases")
    supplier: "Supplier" = Relationship()
    user: User | None = Relationship()
    items: list["PurchaseItem"] = Relationship(back_populates="purchase")


class PurchaseItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    purchase_id: int = Field(foreign_key="purchase.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    unit_cost: float

    purchase: "Purchase" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="purchase_items")  # pyright: ignore[reportUndefinedVariable] # noqa: F821
