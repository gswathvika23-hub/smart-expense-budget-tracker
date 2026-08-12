from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, expenses, budgets

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(expenses.router)
app.include_router(budgets.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}