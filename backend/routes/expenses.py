from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from models.expense import ExpenseCreate, ExpenseInDB, MonthlyAnalytics
from routes.user import get_current_user
from database import db
from bson import ObjectId
from datetime import datetime
import pandas as pd
import io

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=ExpenseInDB)
async def add_expense(expense: ExpenseCreate, current_user: dict = Depends(get_current_user)):
    expense_dict = expense.dict()
    expense_dict["user_id"] = str(current_user["_id"])
    expense_dict["created_at"] = datetime.utcnow()
    
    result = await db.expenses.insert_one(expense_dict)
    expense_dict["_id"] = str(result.inserted_id)
    return expense_dict

@router.get("/", response_model=List[ExpenseInDB])
async def get_expenses(current_user: dict = Depends(get_current_user)):
    cursor = db.expenses.find({"user_id": str(current_user["_id"])})
    expenses = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        expenses.append(doc)
    return expenses

@router.delete("/{expense_id}")
async def delete_expense(expense_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.expenses.delete_one({"_id": expense_id, "user_id": str(current_user["_id"])})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted"}

@router.get("/analytics", response_model=MonthlyAnalytics)
async def get_analytics(current_user: dict = Depends(get_current_user)):
    cursor = db.expenses.find({"user_id": str(current_user["_id"])})
    expenses = []
    async for doc in cursor:
        expenses.append(doc)
    
    total_spent = sum(e["amount"] for e in expenses)
    essential_spent = sum(e["amount"] for e in expenses if e.get("is_essential", True))
    non_essential_spent = total_spent - essential_spent
    
    category_breakdown = {}
    for e in expenses:
        cat = e["category"]
        category_breakdown[cat] = category_breakdown.get(cat, 0) + e["amount"]
        
    return {
        "total_spent": total_spent,
        "essential_spent": essential_spent,
        "non_essential_spent": non_essential_spent,
        "category_breakdown": category_breakdown
    }

@router.post("/upload")
async def upload_transactions(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    contents = await file.read()
    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(contents))
        # Simple parsing logic (assuming Date, Title, Amount columns)
        # In a real app, this would be more robust or use AI to categorize
        expenses_added = 0
        for _, row in df.iterrows():
            try:
                expense = {
                    "title": str(row.get("Title", "Untitled")),
                    "amount": float(row.get("Amount", 0)),
                    "category": str(row.get("Category", "Miscellaneous")),
                    "is_essential": True, # Default
                    "date": datetime.utcnow(),
                    "user_id": str(current_user["_id"]),
                    "created_at": datetime.utcnow()
                }
                await db.expenses.insert_one(expense)
                expenses_added += 1
            except Exception:
                continue
        return {"message": f"Successfully added {expenses_added} expenses"}
    else:
        raise HTTPException(status_code=400, detail="Only CSV files are supported for now")
