from fastapi import APIRouter
from sqlmodel import select, func
from datetime import datetime, timedelta, timezone
from app.db.db import DbSession
from app.db.models.inventory import Sale, Purchase, Inventory, Category

router = APIRouter()


@router.get("/sales")
def sales_chart_data(session: DbSession):
    today = datetime.now(timezone.utc)
    labels = []
    data = []

    sales = session.exec(select(Sale)).all()
    if not sales:
        return {"labels": [], "data": []}

    for i in range(sales.count()):
        day = today - timedelta(days=29 - i)
        label = day.strftime("%Y-%m-%d")
        labels.append(label)
        total = (
            session.exec(
                select(func.sum(Sale.total_amount)).where(
                    func.date(Sale.timestamp) == label
                )
            ).one()[0]
            or 0
        )
        data.append(round(total, 2))
    return {"labels": labels, "data": data}


@router.get("/purchases")
def purchases_chart_data(session: DbSession):
    today = datetime.now(timezone.utc)
    labels = []
    data = []

    purchases = session.exec(select(Purchase)).all()
    if not purchases:
        return {"labels": [], "data": []}

    for i in range(purchases.count()):
        day = today - timedelta(days=29 - i)
        label = day.strftime("%Y-%m-%d")
        labels.append(label)
        total = (
            session.exec(
                select(func.sum(Purchase.total_cost)).where(
                    func.date(Purchase.timestamp) == label
                )
            ).one()[0]
            or 0
        )
        data.append(round(total, 2))
    return {"labels": labels, "data": data}


@router.get("/inventory")
def inventory_chart_data(session: DbSession):
    categories = session.exec(select(Category)).all()
    labels = []
    data = []

    for cat in categories:
        labels.append(cat.name)
        total_qty = (
            session.exec(
                select(func.sum(Inventory.quantity)).where(
                    Inventory.product.has(category_id=cat.id)
                )
            ).one()[0]
            or 0
        )
        data.append(total_qty)

    return {"labels": labels, "data": data}
