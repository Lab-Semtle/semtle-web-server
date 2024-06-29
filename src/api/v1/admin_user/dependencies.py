from fastapi import HTTPException, Depends, Query
from .otp_verification import verify_otp

async def email_verification(email: str = Query(...), otp: str = Query(...)):
    if not verify_otp(email, otp):
        raise HTTPException(status_code=400, detail="이메일 인증 실패")
    return email
