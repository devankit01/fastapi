
from sqlalchemy.orm import Session, joinedload, selectinload, load_only
from .schemas import OrderWithRelatedData
from app.models import Order
from typing import List



def get_order(db: Session, order_id: int) -> OrderWithRelatedData:

    orders = db.query(Order).options(
        selectinload(Order.user).load_only("id", "first_name", "last_name", "email"),
        selectinload(Order.product).load_only("id", "name", "price", "image", "sale"),
        load_only("id", "quantity", "created_at", "updated_at")
        
    ).filter(Order.id == order_id).all()

    return orders


def get_user_orders(db: Session, user_id: int) -> List[OrderWithRelatedData]:

    orders = db.query(Order).options(
        selectinload(Order.product).load_only("id", "name", "price", "image", "sale"),
        load_only("id", "quantity", "created_at", "updated_at")
    ).filter(Order.user_id == user_id).all()

    return orders
