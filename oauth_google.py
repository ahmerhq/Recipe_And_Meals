import os 
from dotenv import load_dotenv

from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
import requests
import urllib.parse

from sqlalchemy.orm import Session
from database_models import User
from database import sessionLocal
from oauth2 import create_token, create_refresh_token

router = APIRouter(tags=["Google Oauth"])

load_dotenv()

GOOGLE_CLIENT_ID= os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI=os.getenv("AUTHORIZED_REDIRECT_URL")


# 1. redirect user to "signin in with google" screen

@router.get("/auth/google/login")
def google_login():
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params= {
        "client_id":GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent" 
    } 

    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)


# 2. handle callback and exchange code for tokens 

@router.get("/auth/google/callback")
def google_callback(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    r = requests.post(token_url, data=data)
    tokens= r.json()

    # Extract tokens from Google
    google_access_token = tokens.get('access_token')
    google_refresh_token = tokens.get('refresh_token')

    # 3. fetch user info
    userinfo = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {google_access_token}"}).json()
    
    email = userinfo["email"]
    username = userinfo.get("name", "GoogleUser")


    # 4. check database 
    db: Session = sessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()

        if not user:
            user= User(
                email=email,
                username=username,
                password=None,
                auth_provider="google",
                google_access_token=google_access_token,
                google_refresh_token=google_refresh_token
            )

            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Update tokens for existing user everytime.
            user.google_access_token = google_access_token
            if google_refresh_token:# ref token issued only once.
                user.google_refresh_token = google_refresh_token 
            db.commit()

        # Create refresh token for app authentication
        payload = {"user_id": user.id}
        refresh_token, refresh_expiry = create_refresh_token(payload)
        
        # Store refresh token in database
        user.refresh_token = refresh_token
        user.refresh_token_expiry = refresh_expiry
        db.commit()

        # Create access token for frontend
        jwt_token = create_token(data={"user_id": user.id})

        # Create response that redirects to frontend with token
        frontend_url = f"http://127.0.0.1:3000/index.html?token={jwt_token}"
        response = RedirectResponse(url=frontend_url)
        
        # Set refresh token cookie (same as manual login)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,   # set to True only in production HTTPS
            samesite="Lax",  # prevent CSRF, but allow redirect
            path="/"        # available at all paths
        )
        return response

    finally:
        db.close()




# # 5. Refresh Google Access Token endpoint
# @router.post("/auth/google/refresh")
# def refresh_google_token(user_id: int):
#     """Refresh Google access token using refresh token"""
#     db: Session = sessionLocal()
#     try:
#         user = db.query(User).filter(User.id == user_id).first()
        
#         if not user or not user.google_refresh_token:
#             return JSONResponse({"error": "User not found or no refresh token"}, status_code=401)
        
#         token_url = "https://oauth2.googleapis.com/token"
#         data = {
#             "client_id": GOOGLE_CLIENT_ID,
#             "client_secret": GOOGLE_CLIENT_SECRET,
#             "refresh_token": user.google_refresh_token,
#             "grant_type": "refresh_token"
#         }
        
#         r = requests.post(token_url, data=data)
#         new_tokens = r.json()
        
#         if "error" in new_tokens:
#             return JSONResponse({"error": "Failed to refresh token"}, status_code=401)
        
#         # Update database with new access token
#         user.google_access_token = new_tokens['access_token']
#         db.commit()
        
#         # Create new JWT token for your app
#         jwt_token = create_token(data={"user_id": user.id})
        
#         return JSONResponse({
#             "access_token": jwt_token,
#             "token_type": "bearer",
#             "expires_in": new_tokens.get('expires_in', 3600)
#         })
#     finally:
#         db.close()










