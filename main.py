import jwt, os
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth.routers import router as auth_routes
from app.api.products.routers import router as product_routes
from app.api.background.routers import router as background_task_routes
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.utils.jwt import get_user

app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
PREFIXES = ["/api/products", "/api/product/"]

# add a middleware that validates the prefixes before continuing for specific urls
class ValidatePrefixMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path.startswith(tuple(PREFIXES)):

            auth_header = request.headers.get("Authorization")

            if not auth_header or "bearer" not in auth_header.lower():
                return JSONResponse({"detail":"Invalid token"},  status_code=status.HTTP_400_BAD_REQUEST)

            """
            can also add auth verification here
            """
            # _, token = auth_header.split(" ")

            # if token is None:
            #     raise JSONResponse({"detail":"Invalid token"},  status_code=status.HTTP_400_BAD_REQUEST)
            # try:
            #     # token = (token.dict()).get("credentials")
            #     payload = jwt.decode(token, JWT_SECRET_KEY,algorithms=["HS256"])
            #     user_id = get_user(user_id=payload.get("data"))

            #     if user_id is None:
            #         return JSONResponse({"detail":"Invalid token"},  status_code=status.HTTP_400_BAD_REQUEST)
            #     response = await call_next(request)
            #     return response

            # except Exception as e:
            #     return JSONResponse({"detail" : "token expired"}, status_code=status.HTTP_400_BAD_REQUEST)

        response = await call_next(request)
        return response


# add middleware
app.add_middleware(ValidatePrefixMiddleware)

# api views
app.include_router(product_routes, tags=['Product'], prefix='/api')
app.include_router(auth_routes, tags=['User'], prefix='/api')
app.include_router(background_task_routes, tags=['Background Tasks'], prefix='/api/background')
