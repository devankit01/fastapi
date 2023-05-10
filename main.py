from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth.routers import router as auth_routes
from app.api.products.routers import router as product_routes
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

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


PREFIXES = ["/api/products", "/api/product"]

# Add a middleware that validates the prefixes before continuing
class ValidatePrefixMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path.startswith(tuple(PREFIXES)):
            auth_header = request.headers.get("Authorization")
            if not auth_header or "bearer" not in auth_header.lower():
                error_message = {"detail": "Invalid authentication token"}
                return JSONResponse(error_message, status_code=status.HTTP_401_UNAUTHORIZED)
        response = await call_next(request)
        return response

# add middleware
app.add_middleware(ValidatePrefixMiddleware)

# product api views
app.include_router(product_routes, tags=['Product'], prefix='/api')
app.include_router(auth_routes, tags=['User'], prefix='/api')
