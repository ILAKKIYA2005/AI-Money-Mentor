from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, user, expenses, ai_advisor, ai_chat, payments
from config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(expenses.router)
app.include_router(ai_advisor.router)
app.include_router(ai_chat.router)
app.include_router(payments.router)

@app.get("/")
async def root():
    return {"message": "Welcome to MONEY MIRROR AI API"}
