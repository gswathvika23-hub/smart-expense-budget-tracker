from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, expenses, budgets, categorize

models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://stellular-klepon-648aef.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(expenses.router)
app.include_router(budgets.router)
app.include_router(categorize.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}