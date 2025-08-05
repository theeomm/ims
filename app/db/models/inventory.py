from sqlmodel import SQLModel, Field, Relationship

from app.db.models.transactions import Purchase, PurchaseItem, Sale, SaleItem


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


# ------------------------ Stock Alerts ------------------------


class StockAlert(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    branch_id: int = Field(foreign_key="branch.id")
    threshold: int = Field(default=5)  # alert when stock <= threshold
    is_active: bool = Field(default=True)

    product: Product = Relationship()
    branch: Branch = Relationship()