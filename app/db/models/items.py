from sqlmodel import Field, SQLModel


class ItemBase(SQLModel):
    name: str = Field()
    price: int = Field()
    description: str | None = Field(default=None)


class Item(ItemBase, table=True):
    id: int = Field(primary_key=True)
