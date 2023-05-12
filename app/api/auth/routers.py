from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.models import get_db
from typing import List
from .schemas import UserSchema, UserReadSchema, UserSignInSchema, RefreshTokenSchema
from app.models import User
from app.utils.jwt import verify_password, get_hashed_password, create_access_token, create_refresh_token, verify_refresh_token, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user
from fastapi.responses import JSONResponse
import jwt
import uuid

router = APIRouter()


class UserView:
    """
    This class contains user apis [ GET, POST, PATCH ]
    """

    @router.post("/user/signup", status_code=status.HTTP_201_CREATED, response_model=UserReadSchema)
    async def signup_user(payload: UserSchema, db: Session = Depends(get_db)):

        data = payload.dict().copy()  # copy data to overwrite
        data["password"] = get_hashed_password(
            data["password"])  # hash password

        # check if user already exists
        user = db.query(User).filter(
            User.email == data["email"]).first()

        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'user already exists with email')

        new_user = User(**data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @router.post("/user/signin", status_code=status.HTTP_200_OK)
    async def signin_user(payload: UserSignInSchema, db: Session = Depends(get_db)):

        # check if user already exists
        user = db.query(User).filter(
            User.email == payload.email).first()

        # check if user exists
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # verify password
        if not verify_password(payload.password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        # create refresh and access tokens
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = {
            "id": str(user.id),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

        # usig JsonResponse because we're using custom reponse
        return JSONResponse(response)

    @router.post("/token/refresh", status_code=status.HTTP_200_OK)
    async def get_access_token(payload: RefreshTokenSchema, db: Session = Depends(get_db)):

        try:
            user_id = verify_refresh_token(payload.refresh_token)

            # create access tokens
            access_token = create_access_token(user_id)

            response = {
                "id": str(user_id),
                "access_token": access_token,
                "token_type": "bearer",
                "expires": 1800
            }

        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired")

        # usig JsonResponse because we're using custom reponse
        return JSONResponse(response)
