from sqlalchemy.dialects.postgresql import UUID
import uuid, os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean, text
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

    __tablename__ = "product"


Base.metadata.create_all(bind=engine)
