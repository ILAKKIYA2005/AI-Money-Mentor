from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ExpenseBase(BaseModel):
    title: str
    amount: float
    category: str  # Rent, Food, etc.
    is_essential: bool = True
    date: datetime = Field(default_factory=datetime.utcnow)
    description: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseInDB(ExpenseBase):
    id: str = Field(..., alias="_id")
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MonthlyAnalytics(BaseModel):
    total_spent: float
    essential_spent: float
    non_essential_spent: float
    category_breakdown: dict
