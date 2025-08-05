from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlmodel import select

from app.db.crud.inventory import add_product
from app.db.db import DbSession
from app.db.models.inventory import Inventory, Product
from app.dependencies import templates
from app.utils import check_and_trigger_alert, log_action


router = APIRouter(default_response_class=HTMLResponse)


@router.post("/products/create", name="inventory:create_product")
def create_product(product: Product, session: DbSession):
    prod = add_product(product, session)
    context = {"product": prod, "request": Request}
    return templates.TemplateResponse("inventory/product_detail.html", context)


@router.get("/products/{product_id}", name="inventory:product_detail")
def get_product_detail(product_id: int, session: DbSession):
    product = session.exec(select(Product).where(Product.id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    context = {"product": product, "request": Request}
    return templates.TemplateResponse("inventory/product_detail.html", context)


@router.get("/products", name="inventory:list_products")
def list_products(session: DbSession):
    products = session.exec(select(Product)).all()
    context = {"products": products, "request": Request}
    return templates.TemplateResponse("inventory/product_list.html", context)


@router.post("/add", name="inventory:add_inventory")
def update_inventory(
    branch_id: int,
    product_id: int,
    quantity: int,
    session: DbSession,
):
    inv = session.exec(
        select(Inventory).where(
            Inventory.branch_id == branch_id,
            Inventory.product_id == product_id,
        )
    ).first()

    if inv:
        inv.quantity += quantity
    else:
        inv = Inventory(
            branch_id=branch_id,
            product_id=product_id,
            quantity=quantity,
        )
        session.add(inv)

    session.commit()
    check_and_trigger_alert(session, branch_id, product_id)
    log_action(
        session,
        user_id=1,
        action="UPDATE_STOCK",
        model="Inventory",
        model_id=inv.id,
    )
    return inv
