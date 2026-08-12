from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from ..dependencies import get_db, get_current_user
from .. import models, schemas

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.post("/", response_model=schemas.BudgetOut)
def create_budget(
    budget: schemas.BudgetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    category = db.query(models.Category).filter(models.Category.id == budget.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    existing = db.query(models.Budget).filter(
        models.Budget.user_id == current_user.id,
        models.Budget.category_id == budget.category_id,
        models.Budget.month == budget.month,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Budget already exists for this category and month")

    new_budget = models.Budget(
        user_id=current_user.id,
        category_id=budget.category_id,
        monthly_limit=budget.monthly_limit,
        month=budget.month,
    )
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget


@router.get("/", response_model=List[schemas.BudgetOut])
def list_budgets(
    month: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.Budget).filter(models.Budget.user_id == current_user.id)
    if month:
        query = query.filter(models.Budget.month == month)
    return query.all()


@router.get("/status", response_model=List[schemas.BudgetStatusOut])
def budget_status(
    month: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.Budget).filter(models.Budget.user_id == current_user.id)
    if month:
        query = query.filter(models.Budget.month == month)
    budgets = query.all()

    results = []
    for b in budgets:
        spent = db.query(func.coalesce(func.sum(models.Expense.amount), 0)).filter(
            models.Expense.user_id == current_user.id,
            models.Expense.category_id == b.category_id,
            func.to_char(models.Expense.date, 'YYYY-MM') == b.month,
        ).scalar()
        spent = float(spent)
        monthly_limit = float(b.monthly_limit)
        remaining = monthly_limit - spent
        percent_used = (spent / monthly_limit * 100) if monthly_limit > 0 else 0

        results.append(schemas.BudgetStatusOut(
            id=b.id,
            category_id=b.category_id,
            monthly_limit=b.monthly_limit,
            month=b.month,
            spent=spent,
            remaining=remaining,
            percent_used=round(percent_used, 2),
        ))
    return results


@router.put("/{budget_id}", response_model=schemas.BudgetOut)
def update_budget(
    budget_id: int,
    budget_update: schemas.BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    budget = db.query(models.Budget).filter(
        models.Budget.id == budget_id,
        models.Budget.user_id == current_user.id,
    ).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    for field, value in budget_update.dict(exclude_unset=True).items():
        setattr(budget, field, value)

    db.commit()
    db.refresh(budget)
    return budget


@router.delete("/{budget_id}")
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    budget = db.query(models.Budget).filter(
        models.Budget.id == budget_id,
        models.Budget.user_id == current_user.id,
    ).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    db.delete(budget)
    db.commit()
    return {"detail": "Budget deleted successfully"}