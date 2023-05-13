from fastapi import Response, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from app.models import get_db
from typing import List
from .schemas import ProductReadSchema, ProductSchema, ProductUpdate, OrderSchema
from app.models import Product, Order
from app.utils.s3 import s3_client
from app.utils.jwt import authenticate_user
from datetime import date
import uuid, os
from .utils import get_order, get_user_orders


router = APIRouter()
AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")

class ProductView:
    """
    This class contains product apis [ GET, POST, PATCH and DELETE ]
    """

    @router.get("/products", response_model=List[ProductReadSchema])
    # get user_id from token
    async def get_products(db: Session = Depends(get_db), search: str = "",  user_id: int = Depends(authenticate_user)):
        # notes = db.query(Product).filter(Product.name.contains(search)).limit(limit).offset(skip).all() : operation in query
        products = db.query(Product).filter(
            Product.name.contains(search)).all()
        return products

    @router.post("/products", status_code=status.HTTP_201_CREATED)
    async def create_product(payload: ProductSchema, db: Session = Depends(get_db),  user_id: int = Depends(authenticate_user)):
        new_product = Product(**payload.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    @router.get("/product")
    async def get_product(id: uuid.UUID, db: Session = Depends(get_db),  user_id: int = Depends(authenticate_user)):
        product = db.query(Product).filter(
            Product.id == id).first()  # query to get single data
        return product

    @router.patch('/product/{id}')
    async def update_product(id: uuid.UUID, payload: ProductUpdate, db: Session = Depends(get_db),  user_id: int = Depends(authenticate_user)):
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
    async def delete_post(id: uuid.UUID, db: Session = Depends(get_db),  user_id: int = Depends(authenticate_user)):
        product_query = db.query(Product).filter(
            Product.id == id)  # query to get single data
        product = product_query.first()

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No product with this id: {id} found')
        product_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


class ImageView:

    @router.post("/product/upload/image/")
    async def upload_image(file: UploadFile = File(...),  user_id: int = Depends(authenticate_user)):
        """
        Upload an image file to S3 bucket.
        """
        valid_extensions = ["png", "jpg", "jpeg"]
        if (file.content_type).split("/")[-1] in valid_extensions:

            # generate a unique key for the file
            random_uuid = str(uuid.uuid4()) + "." + \
                (file.content_type).split("/")[-1]
            file_key = f"images/{str(date.today())}/{random_uuid}"

            try:
                # upload the file to S3
                s3_client.upload_fileobj(file.file, AWS_BUCKET_NAME, file_key)
            except Exception as e:
                raise HTTPException(detail=str(
                    e), status_code=status.HTTP_406_NOT_ACCEPTABLE)

            # return the uploaded file URL
            file_url = f"https://fastapi-images.s3.amazonaws.com/{file_key}"
            return {"detail": "file uploaded successfully", "file_url": file_url}

        else:
            raise HTTPException(detail="Invalid image format. Only .png and .jpg files are allowed.",
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)


class OrderView:
    @router.post("/order")
    def create_order(payload: OrderSchema, db: Session = Depends(get_db),  user_id: int = Depends(authenticate_user)):
        new_order = Order(**payload.dict())
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order

    @router.get("/orders", )
    def get_users_all_orders( id: uuid.UUID, db: Session = Depends(get_db), user_id: int = Depends(authenticate_user)):
        order = get_user_orders(db, user_id=id)  # query to get all orders data
        return order
    
    @router.get("/order", )
    def get_single_order(id: uuid.UUID, db: Session = Depends(get_db),  user_id: int = Depends(authenticate_user)):
        order = get_order(db, order_id=id)  # query to get single data
        return order
