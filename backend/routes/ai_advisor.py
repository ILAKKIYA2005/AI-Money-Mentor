from fastapi import APIRouter, Depends
from services.ai_agent import ai_agent
from routes.user import get_current_user
from routes.expenses import get_expenses
from database import db

router = APIRouter(prefix="/ai", tags=["ai"])

@router.get("/insights")
async def get_insights(current_user: dict = Depends(get_current_user)):
    profile_dict = current_user.get("profile", {})
    from models.user import UserProfile
    profile = UserProfile(**profile_dict) if profile_dict else UserProfile()
    
    expenses_cursor = db.expenses.find({"user_id": str(current_user["_id"])})
    expenses = []
    async for doc in expenses_cursor:
        expenses.append(doc)
    
    total_spent = sum(e["amount"] for e in expenses)
    salary = profile.monthly_salary or 0
    
    health_score = ai_agent.calculate_health_score(salary, total_spent, profile.risk_level)
    sip_suggestion = ai_agent.suggest_sip(salary, total_spent)
    schemes = ai_agent.recommend_schemes(profile)
    reminders = ai_agent.predict_reminders(expenses, schemes)
    
    return {
        "health_score": health_score,
        "sip_suggestion": sip_suggestion,
        "schemes": schemes,
        "reminders": reminders,
        "insights": f"Your current savings rate is {round(((salary - total_spent)/salary)*100, 2) if salary > 0 else 0}%."
    }
