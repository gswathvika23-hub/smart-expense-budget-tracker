from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_current_user
from .. import models, schemas

router = APIRouter(prefix="/categorize", tags=["categorize"])

# Keyword map: category name -> list of keywords to match against description
CATEGORY_KEYWORDS = {
    "Food": [
        "restaurant", "food", "grocery", "groceries", "coffee", "cafe",
        "starbucks", "swiggy", "zomato", "lunch", "dinner", "breakfast",
        "pizza", "burger", "snack", "bakery", "tea", "milk", "vegetables",
    ],
    "Travel": [
        "uber", "ola", "taxi", "cab", "flight", "airline", "train",
        "bus", "petrol", "fuel", "diesel", "metro", "travel", "trip",
        "airport", "railway", "parking", "toll",
    ],
    "Shopping": [
        "amazon", "flipkart", "mall", "shopping", "clothes", "shoes",
        "electronics", "myntra", "store", "purchase", "shirt", "dress",
    ],
    "Bills": [
        "electricity", "water bill", "wifi", "internet", "rent",
        "phone bill", "recharge", "insurance", "emi", "subscription",
        "netflix", "gas bill", "maintenance",
    ],
}


@router.post("/suggest", response_model=schemas.CategorizeResponse)
def suggest_category(
    request: schemas.CategorizeRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    description_lower = request.description.lower()

    best_match_name = None
    best_match_count = 0

    for category_name, keywords in CATEGORY_KEYWORDS.items():
        match_count = sum(1 for kw in keywords if kw in description_lower)
        if match_count > best_match_count:
            best_match_count = match_count
            best_match_name = category_name

    if best_match_name is None:
        best_match_name = "Shopping"
        confidence = 0.2
    else:
        confidence = min(0.5 + best_match_count * 0.2, 0.95)

    category = db.query(models.Category).filter(
        models.Category.name == best_match_name
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail=f"Category '{best_match_name}' not found in database")

    return schemas.CategorizeResponse(
        suggested_category_id=category.id,
        suggested_category_name=category.name,
        confidence=round(confidence, 2),
    )