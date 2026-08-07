from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
   

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    category_id: int
    date: date

class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    category_id: Optional[int] = None
    date: Optional[date] = None

class ExpenseOut(BaseModel):
    id: int
    description: str
    amount: float
    category_id: int
    date: date

    class Config:
        orm_mode = True