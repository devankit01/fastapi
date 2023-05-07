from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from views import product

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

# product api views
app.include_router(product.router, tags=['Product'], prefix='/api')

