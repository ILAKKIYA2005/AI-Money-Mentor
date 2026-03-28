from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserProfile(BaseModel):
    age: Optional[int] = None
    occupation: Optional[str] = None
    monthly_salary: Optional[float] = 0.0
    income_sources: List[str] = []
    location: str = "India"
    financial_goals: List[str] = []
    risk_level: str = "Moderate"  # Low, Moderate, High

class UserInDB(UserBase):
    id: str = Field(..., alias="_id")
    hashed_password: str
    profile: Optional[UserProfile] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
