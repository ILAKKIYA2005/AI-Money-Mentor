from typing import List, Dict
from models.user import UserProfile
from models.expense import ExpenseInDB
from datetime import datetime, timedelta

class AIAgent:
    @staticmethod
    def calculate_health_score(salary: float, total_expenses: float, risk_level: str) -> int:
        if salary <= 0: return 0
        savings_ratio = (salary - total_expenses) / salary
        score = int(savings_ratio * 100)
        
        # Adjust based on risk level
        if risk_level == "High": score -= 5
        elif risk_level == "Low": score += 5
        
        return max(0, min(100, score))

    @staticmethod
    def suggest_sip(salary: float, total_expenses: float) -> float:
        savings = salary - total_expenses
        if savings <= 0: return 0
        return round(savings * 0.3, 2) # Suggest 30% of savings for SIP

    @staticmethod
    def recommend_schemes(profile: UserProfile) -> List[Dict]:
        schemes = []
        occ = profile.occupation.lower() if profile.occupation else ""
        age = profile.age or 0
        salary = profile.monthly_salary or 0
        
        # Indian Government Schemes (Examples)
        if "farmer" in occ or "agriculture" in occ:
            schemes.append({
                "name": "PM-KISAN",
                "description": "Direct income support of ₹6,000 per year to all landholding farmer families.",
                "link": "https://pmkisan.gov.in/",
                "reason": f"As someone in {occ}, you qualify for fixed annual income support to stabilize your farm earnings."
            })
            schemes.append({
                "name": "PM Fasal Bima Yojana",
                "description": "Crop insurance scheme for farmers against natural calamities.",
                "link": "https://pmfby.gov.in/",
                "reason": "Protects your high-input costs against unpredictable weather patterns typical in agriculture."
            })
        
        if "student" in occ or age < 25:
            schemes.append({
                "name": "PM Vidyalakshmi",
                "description": "Single window for Students to access Information and fill a Common Education Loan Application.",
                "link": "https://www.vidyalakshmi.co.in/",
                "reason": f"Perfect for a {age}-year-old student looking for centralized education financing without multiple applications."
            })
            schemes.append({
                "name": "Skill India Mission",
                "description": "Training and skill development programs for youth.",
                "link": "https://www.skillindia.gov.in/",
                "reason": "Since you are in a learning phase, this mission helps bridge the gap between your studies and industry-ready skills."
            })
        
        if salary < 30000:
            schemes.append({
                "name": "PM Shram Yogi Maan-dhan",
                "description": "Pension scheme for unorganized workers with monthly income up to ₹15,000.",
                "link": "https://labour.gov.in/pm-sym",
                "reason": "Based on your current income tier, this ensures long-term social security for your retirement."
            })
            
        # Universal Schemes for all users
        schemes.append({
            "name": "Public Provident Fund (PPF)",
            "description": "Government-backed savings with 7.1% interest (2025-26). EEE tax status - Invest up to ₹1.5L/yr.",
            "link": "https://www.indiapost.gov.in/VAS/Pages/Form.aspx",
            "reason": "A must-have for every Indian citizen to build a tax-free retirement corpus with 100% principal security."
        })
        schemes.append({
            "name": "National Pension System (NPS)",
            "description": "Market-linked pension scheme. Extra ₹50,000 tax deduction under 80CCD(1B).",
            "link": "https://enps.nsdl.com/eNPS/LandingPage.html",
            "reason": "Perfect for inflation-beating retirement growth. Now allows 60% tax-free lump sum withdrawal at age 60."
        })
            
        return schemes[:6] # Limit to top 6

    @staticmethod
    def predict_reminders(expenses: List[Dict], schemes: List[Dict] = None) -> List[Dict]:
        reminders = []
        for exp in expenses:
            title = exp.get("title", "").lower()
            if any(k in title for k in ["recharge", "bill", "emi", "subscription"]):
                reminders.append({
                    "title": f"Predictive: {exp['title']} due soon",
                    "due_date": (datetime.utcnow() + timedelta(days=5)).strftime("%Y-%m-%d"),
                    "type": "Predictive"
                })
        
        if schemes:
            for scheme in schemes[:2]:
                reminders.append({
                    "title": f"New Scheme: {scheme['name']}",
                    "due_date": datetime.utcnow().strftime("%Y-%m-%d"),
                    "type": "Scheme Alert"
                })
        return reminders
                
    @staticmethod
    def chat_response(message: str, profile: Dict, expenses: List[Dict]) -> str:
        msg = message.lower()
        salary = profile.get("monthly_salary", 0)
        total_spent = sum(e["amount"] for e in expenses)
        savings = salary - total_spent
        
        if "hello" in msg or "hi" in msg:
            return f"Hello! I am your Money Mirror AI. I see your current savings are ₹{savings}. How can I help you grow your wealth today?"
        
        if "spending" in msg or "expense" in msg:
            top_expense = max(expenses, key=lambda x: x["amount"]) if expenses else None
            if top_expense:
                return f"You've spent a total of ₹{total_spent} this month. Your highest expense was '{top_expense['title']}' at ₹{top_expense['amount']}. Maybe we can optimize that?"
            return "You haven't recorded any expenses yet! Add some so I can analyze your habits."
            
        if "save" in msg or "invest" in msg:
            if savings > 10000:
                return f"With ₹{savings} in savings, I recommend putting ₹{int(savings * 0.4)} into a High-Yield SIP and ₹{int(savings * 0.2)} into your PPF for tax-free growth."
            return "Focus on building an emergency fund of at least 3 months' salary before aggressive investing."
            
        if "scheme" in msg or "government" in msg:
            return "Based on your profile, I've highlighted specific Indian Govt schemes like PPF and NPS in your dashboard. Would you like me to explain one of them?"

        if "risk" in msg:
            return f"Your current risk profile is '{profile.get('risk_level', 'Moderate')}'. This is great for your age of {profile.get('age', 25)}. We can adjust this in settings if your goals change."

        return "That's a great question! While I'm in prototype mode, I can help you with spending analysis, investment tips, and scheme explanations. Ask me about your expenses!"

ai_agent = AIAgent()
