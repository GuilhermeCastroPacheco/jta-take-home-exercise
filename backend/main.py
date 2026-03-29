from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, products, search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://jta-take-home-exercise.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users")
app.include_router(products.router, prefix="/products")
app.include_router(search.router)