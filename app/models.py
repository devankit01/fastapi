from sqlalchemy.dialects.postgresql import UUID
import uuid, os
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from dotenv import load_dotenv
load_dotenv()

# db connection
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# make db session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# return db session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Product(Base):
    """
    Product model contains id, name, price, stock and sale
    """
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    price = Column(Integer)
    stock = Column(Integer)
    sale = Column(Boolean, default=False)
    image = Column(String, default="")

    __tablename__ = "product"
    
    # Define relationship with orders
    orders = relationship("Order", back_populates="product")


class User(Base):
    """
    """
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    
    
    # Define relationship with orders
    orders = relationship("Order", back_populates="user")

    __tablename__ = "users"


class Order(Base):

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    quantity = Column(Integer)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Define relationships with user and product
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
    
    __tablename__ = 'orders'
    
    
Base.metadata.create_all(bind=engine)
