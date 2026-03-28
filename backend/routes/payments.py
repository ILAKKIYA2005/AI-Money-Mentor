from fastapi import APIRouter, Depends
from pydantic import BaseModel
from routes.user import get_current_user

router = APIRouter(prefix="/payments", tags=["payments"])

class UPIRequest(BaseModel):
    amount: float
    note: str = "Investment via Money Mirror"

@router.post("/generate-upi")
async def generate_upi_link(request: UPIRequest, current_user: dict = Depends(get_current_user)):
    # Standard UPI URI format
    # Replace with a real business VPA in production
    vpa = "moneymirror@ybl" 
    name = "Money Mirror AI"
    
    upi_uri = f"upi://pay?pa={vpa}&pn={name}&am={request.amount}&cu=INR&tn={request.note}"
    
    return {
        "upi_uri": upi_uri,
        "vpa": vpa,
        "amount": request.amount
    }
