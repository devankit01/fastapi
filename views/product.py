from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from models import get_db
from typing import List
from schema.product import ProductReadSchema, ProductSchema, ProductUpdate
from models import Product
import uuid

router = APIRouter()


class ProductView:
    """
    This class contains product apis [ GET, POST, PATCH and DELETE ]
    """

    @router.get("/products", response_model=List[ProductReadSchema])
    async def get_products(db: Session = Depends(get_db), search: str = "", ):
        # notes = db.query(Product).filter(Product.name.contains(search)).limit(limit).offset(skip).all() : operation in query
        products = db.query(Product).filter(
            Product.name.contains(search)).all()
        return products

    @router.post("/products", status_code=status.HTTP_201_CREATED)
    async def create_product(payload: ProductSchema, db: Session = Depends(get_db)):
        new_product = Product(**payload.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    @router.get("/product/{id}")
    async def get_product(id: uuid.UUID, db: Session = Depends(get_db)):
        product = db.query(Product).filter(
            Product.id == id).first()  # query to get single data
        return product

    @router.patch('/product/{id}')
    async def update_note(id: uuid.UUID, payload: ProductUpdate, db: Session = Depends(get_db)):
        product_query = db.query(Product).filter(
            Product.id == id)  # query to get single data
        product = product_query.first()

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No product with this id: {id} found')

        update_data = payload.dict(exclude_unset=True)
        product_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(product)
        return product

    @router.delete('/product/{id}')
    async def delete_post(id: uuid.UUID, db: Session = Depends(get_db)):
        product_query = db.query(Product).filter(
            Product.id == id)  # query to get single data
        product = product_query.first()

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No product with this id: {id} found')
        product_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
