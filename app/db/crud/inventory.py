from fastapi import HTTPException
from sqlmodel import select
from app.db.db import DbSession
from app.db.models.inventory import Product
from app.dependencies import get_current_user
from app.utils import log_action


def product_exists(session: DbSession, product_name: str) -> bool:
    """Check if a product with the given name already exists."""
    return (
        session.exec(select(Product).where(Product.name == product_name)).first()
        is not None
    )


def raise_product_exists_exception():
    """Raise an HTTP exception if the product already exists."""
    if product_exists:
        raise HTTPException(status_code=400, detail="Product already exists")


def add_product(product: Product, session: DbSession):
    """Create a new product in the inventory."""
    raise_product_exists_exception(session, product.name)

    user = get_current_user(session)

    session.add(product)
    session.commit()
    session.refresh(product)
    log_action(
        session,
        user_id=user.id,
        action="CREATE_PRODUCT",
        model="Product",
        model_id=product.id,
    )
    return product
