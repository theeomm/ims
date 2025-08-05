from datetime import datetime
from sqlmodel import select
from app.db.db import DbSession
from app.db.models.inventory import Inventory, StockAlert
from app.db.models.audit import AuditTrail


def log_action(
    session: DbSession,
    user_id: int,
    action: str,
    model: str,
    model_id: int,
    description: str = "",
):
    """Log an action in the audit trail."""
    log = AuditTrail(
        user_id=user_id,
        action=action,
        model=model,
        model_id=model_id,
        description=description,
        timestamp=datetime.now(datetime),
    )
    session.add(log)
    session.commit()


def check_and_trigger_alert(session: DbSession, branch_id: int, product_id: int):
    """Check inventory levels and trigger alerts if necessary."""
    inventory = session.exec(
        select(Inventory).where(
            Inventory.branch_id == branch_id, Inventory.product_id == product_id
        )
    ).first()

    alert = session.exec(
        select(StockAlert).where(
            StockAlert.branch_id == branch_id,
            StockAlert.product_id == product_id,
            StockAlert.is_active,
        )
    ).first()

    if alert and inventory and inventory.quantity <= alert.threshold:
        # TODO: Implement Email or SMS notification logic here
        print(
            f"⚠️ STOCK ALERT: Product {product_id} in Branch {branch_id} is low ({inventory.quantity})"
        )


