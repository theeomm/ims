from fastapi import APIRouter, Depends
from app.db.db import DbSession
from app.db.models.inventory import Sale, SaleItem, Purchase, PurchaseItem
from app.dependencies import get_current_user
from app.utils import log_action, check_and_trigger_alert

router = APIRouter()

# ------------------- Sales -------------------


@router.post("/sales/create")
def create_sale(
    items: list[SaleItem],
    branch_id: int,
    session: DbSession,
    user=Depends(get_current_user),
):
    """Create a new sale and update inventory."""
    total = sum(item.quantity * item.unit_price for item in items)
    sale = Sale(
        branch_id=branch_id,
        total_amount=total,
        user_id=user.id,
    )
    session.add(sale)
    session.commit()
    for item in items:
        item.sale_id = sale.id
        session.add(item)
        check_and_trigger_alert(session, branch_id, item.product_id)
    session.commit()
    log_action(
        session,
        user.id,
        "CREATE_SALE",
        "Sale",
        sale.id,
        "New sale recorded",
    )
    return {"message": "Sale completed", "sale_id": sale.id}


# ------------------- Purchases -------------------


@router.post("/purchases/create")
def create_purchase(
    items: list[PurchaseItem],
    branch_id: int,
    supplier_id: int,
    session: DbSession,
    user=Depends(get_current_user),
):
    """Create a new purchase and update inventory."""
    total = sum(item.quantity * item.unit_cost for item in items)
    purchase = Purchase(
        branch_id=branch_id,
        supplier_id=supplier_id,
        total_cost=total,
        user_id=user.id,
    )
    session.add(purchase)
    session.commit()
    for item in items:
        item.purchase_id = purchase.id
        session.add(item)
    session.commit()
    log_action(
        session,
        user.id,
        "CREATE_PURCHASE",
        "Purchase",
        purchase.id,
        "New purchase recorded",
    )
    return {"message": "Purchase completed", "purchase_id": purchase.id}
