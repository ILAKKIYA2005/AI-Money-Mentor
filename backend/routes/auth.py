from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import settings
from models.user import UserCreate, UserInDB, Token, TokenData, UserBase
from database import db
from bson import ObjectId

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/signup", response_model=UserBase)
async def signup(user: UserCreate):
    print(f"DEBUG: Signup attempt for email: {user.email}")
    try:
        existing_user = await db.users.find_one({"email": user.email})
        if existing_user:
            print(f"DEBUG: Email {user.email} already exists")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        print(f"DEBUG: Hashing password for {user.email}")
        hashed_password = get_password_hash(user.password)
        user_dict = user.dict()
        del user_dict["password"]
        user_dict["hashed_password"] = hashed_password
        user_dict["profile"] = None
        user_dict["created_at"] = datetime.utcnow()
        
        print(f"DEBUG: Inserting user into MockDB")
        result = await db.users.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        print(f"DEBUG: Signup successful for {user.email}")
        return user_dict
    except Exception as e:
        print(f"DEBUG: Signup error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
