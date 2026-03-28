from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from models.user import UserProfile, UserInDB
from routes.auth import oauth2_scheme
from database import db
from config import settings
from bson import ObjectId

router = APIRouter(prefix="/user", tags=["user"])

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print(f"DEBUG: Validating token: {token[:10]}...")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        print(f"DEBUG: Token payload: {payload}")
        email: str = payload.get("sub")
        if email is None:
            print("DEBUG: No sub in payload")
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(f"DEBUG: Token validation error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await db.users.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: dict = Depends(get_current_user)):
    profile = current_user.get("profile")
    if not profile:
        return UserProfile()
    return profile

@router.post("/profile", response_model=UserProfile)
async def update_profile(profile: UserProfile, current_user: dict = Depends(get_current_user)):
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$set": {"profile": profile.dict()}}
    )
    return profile
