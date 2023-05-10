from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
# from jose import jwt
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer
from app.models import User
from sqlalchemy.orm import Session
from app.models import get_db
from fastapi import HTTPException, Depends

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']     # should be kept secret
# should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """ 
    Hash the password
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """ 
    Verify password
    """
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any]) -> str:
    """ 
    Create access token
    """
    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "data": str(subject)}
    access_token = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return access_token


def create_refresh_token(subject: Union[str, Any]) -> str:
    """ 
    Create refresh token
    """
    expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "data": str(subject)}
    refresh_token = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return refresh_token


async def get_user(user_id : str, db: Session = Depends(get_db)) :
    """ 
    Retrieve user from db using using id
    """
    return db.query(User).filter(User.id ==user_id).first()


# Define an instance of HTTPBearer for authentication
auth_scheme = HTTPBearer()

# Define a function to authenticate the user using JWT token
async def authenticate_user(token: str = Security(auth_scheme)) -> int:
    """ 
    Validate token
    """
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    try:
        token = (token.dict()).get("credentials")
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = get_user(user_id=payload.get("data"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")