from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database_models import User
from database import get_db
from sqlalchemy.orm import Session
from utils import verify_pass
from oauth2 import create_token



router = APIRouter(tags=["Login"])

@router.post("/login")
def login(uc:OAuth2PasswordRequestForm= Depends(), db:Session = Depends(get_db)):
    db_user = db.query(User).filter((User.email == uc.username) | (User.username == uc.username) ).first()

    if not db_user or not verify_pass(uc.password, db_user.password):
        raise HTTPException(status_code=404, detail="Invalid Email or password")
    
    payload = {"user_id": db_user.id}
    token = create_token(payload)


    return {"access_token": token, "token_type":"bearer"}




