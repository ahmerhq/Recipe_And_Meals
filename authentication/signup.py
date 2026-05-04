from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import userCreate, UserResponse
from database import get_db
from database_models import User
from utils import hash_pass


router = APIRouter(tags=["SignUp"])

@router.post("/signup", response_model=UserResponse)

def signup(uc: userCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email== uc.email).first()

    if db_user:
        raise HTTPException(status_code=409, detail="User already exist with this email")
    
    hashed_pass = hash_pass(uc.password)
    uc.password = hashed_pass

    new_user = User(**uc.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user















