from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from routes.user import get_current_user
from services.ai_agent import ai_agent
from database import db

router = APIRouter(prefix="/ai", tags=["ai"])

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_with_ai(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    profile = current_user.get("profile", {})
    
    # Get user expenses for context
    expenses_cursor = db.expenses.find({"user_id": current_user["_id"]})
    expenses = await expenses_cursor.to_list(length=100)
    
    response = ai_agent.chat_response(request.message, profile, expenses)
    return {"response": response}
