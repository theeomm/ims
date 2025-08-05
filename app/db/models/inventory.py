from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone

from app.db.models.users import User


class Branch(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    location: str

    inventories: list["Inventory"] = Relationship(back_populates="branch")
    sales: list["Sale"] = Relationship(back_populates="branch")
    purchases: list["Purchase"] = Relationship(back_populates="branch")


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None

    products: list["Product"] = Relationship(back_populates="category")


class Supplier(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    contact_info: str | None = None

    products: list["Product"] = Relationship(back_populates="supplier")


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    sku: str = Field(index=True, unique=True)
    barcode: str | None = Field(default=None, index=True, unique=True)
    description: str | None = None
    price: float
    is_active: bool = Field(default=True)

    category_id: int | None = Field(default=None, foreign_key="category.id")
    supplier_id: int | None = Field(default=None, foreign_key="supplier.id")

    category: Category | None = Relationship(back_populates="products")
    supplier: Supplier | None = Relationship(back_populates="products")
    inventories: list["Inventory"] = Relationship(back_populates="product")
    sale_items: list["SaleItem"] = Relationship(back_populates="product")
    purchase_items: list["PurchaseItem"] = Relationship(back_populates="product")


class Inventory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    branch_id: int = Field(foreign_key="branch.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int

    branch: "Branch" = Relationship(back_populates="inventories")
    product: "Product" = Relationship(back_populates="inventories")


class Sale(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    branch_id: int = Field(foreign_key="branch.id")
    user_id: int | None = Field(default=None, foreign_key="user.id")
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    total_amount: float

    branch: Branch = Relationship(back_populates="sales")
    items: list["SaleItem"] = Relationship(back_populates="sale")
    user: User | None = Relationship()


class SaleItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sale_id: int = Field(foreign_key="sale.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    unit_price: float

    sale: Sale = Relationship(back_populates="items")
    product: Product = Relationship(back_populates="sale_items")


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

    purchase: Purchase = Relationship(back_populates="items")
    product: Product = Relationship(back_populates="purchase_items")


# ------------------------ Stock Alerts ------------------------


class StockAlert(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    branch_id: int = Field(foreign_key="branch.id")
    threshold: int = Field(default=5)  # alert when stock <= threshold
    is_active: bool = Field(default=True)

    product: Product = Relationship()
    branch: Branch = Relationship()
