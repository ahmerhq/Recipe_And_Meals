from fastapi import APIRouter, HTTPException, Depends, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from database_models import User
from database import get_db
from sqlalchemy.orm import Session
from utils import verify_pass
from oauth2 import create_token, create_refresh_token, verify_refresh_token
from models import TokenResponse, RefreshTokenRequest
from datetime import datetime

router = APIRouter(tags=["Login"])

@router.post("/login", response_model=TokenResponse)
def login(response: Response, uc:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    db_user = db.query(User).filter((User.email == uc.username) | (User.username == uc.username) ).first()

    if not db_user or not verify_pass(uc.password, db_user.password):
        raise HTTPException(status_code=404, detail="Invalid Email or password")
    
    payload = {"user_id": db_user.id}
    access_token = create_token(payload)
    refresh_token, refresh_expiry = create_refresh_token(payload)
    
    # Store refresh token in database
    db_user.refresh_token = refresh_token
    db_user.refresh_token_expiry = refresh_expiry
    db.commit()

    response.set_cookie(
        key= "refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,   # set to True only in production HTTPS
        samesite="Lax",  # prevent CSRF
        path="/"  # available at all paths
    )

    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh(response: Response, request: Request, db: Session = Depends(get_db)):
    """Refresh the access token using a valid refresh token"""
    
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "bearer"},
    )

    #get refresh token from cookie
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise credential_exception
    
    # Verify the refresh token JWT
    token_data_obj = verify_refresh_token(refresh_token, credential_exception)
    
    # Get user from database
    user = db.query(User).filter(User.id == token_data_obj.id).first()
    if not user or user.refresh_token != refresh_token:
        raise credential_exception
    

    # Check if refresh token has expired
    if user.refresh_token_expiry and user.refresh_token_expiry < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has expired")
    
    # Create new access token only (don't rotate refresh token to avoid race conditions)
    payload = {"user_id": user.id}
    new_access_token = create_token(payload)
    
    # Don't rotate refresh token on every call - only create new access token
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


# Refresh token is no longer returned in JSON. It’s stored in a secure HttpOnly cookie.  Line 29 - 54 - 81
@router.post("/logout")
def logout(response: Response):
    """Logout by clearing the refresh token cookie"""
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,   # set to True only in production HTTPS
        samesite="Lax",
        path="/"
    )
    return {"message": "Logged out successfully"}