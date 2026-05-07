from jose import JWTError, jwt
from datetime import datetime, timedelta
from models import token_data
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from sqlalchemy.orm import Session
from database_models import User
import os 
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION_TIME = int(os.getenv("EXPIRATION_TIME"))
REFRESH_EXPIRATION_TIME = int(os.getenv("REFRESH_EXPIRATION_TIME"))

# creates access token
def create_token(data:dict):
    to_encode = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp": exp})
    jwt_token = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token



# creates refresh token
def create_refresh_token(data:dict):
    to_encode = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=REFRESH_EXPIRATION_TIME)
    to_encode.update({"exp": exp})
    jwt_token = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token, exp



# verifying access token
def verrify_token(token, credential_exception):
    try:
        decode = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        us_id = decode.get("user_id")

        if not us_id:
            raise HTTPException(status_code=404, detail="invalid user")
        return token_data(id=us_id)
    
    except JWTError:
        raise credential_exception


# verifying refresh token
def verify_refresh_token(token, credential_exception):
    try:
        decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        us_id = decode.get("user_id")

        if not us_id:
            raise HTTPException(status_code=404, detail="invalid user")
        return token_data(id=us_id)
    
    except JWTError:
        raise credential_exception


auth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def allow_access(token:str = Depends(auth2_scheme), db:Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail= "User deleted or does not exist.",
        headers={"WWW-Authenticate": "bearer"},
    )

    new_token = verrify_token(token, credential_exception)
    user_query = db.query(User).filter(User.id == new_token.id).first()

    if not user_query:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    
    return user_query



# function that verifies that ref token is valid.
# refresh_token_scheme = OAuth2PasswordBearer(tokenUrl="refresh")
# def verify_refresh_token_dependency(token: str = Depends(refresh_token_scheme), db: Session = Depends(get_db)):
#     credential_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid refresh token",
#         headers={"WWW-Authenticate": "bearer"},
#     )
    
#     token_data_obj = verify_refresh_token(token, credential_exception)
    
#     user = db.query(User).filter(User.id == token_data_obj.id).first()
    
#     if not user or user.refresh_token != token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired refresh token"
#         )
    
#     if user.refresh_token_expiry and user.refresh_token_expiry < datetime.utcnow():
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Refresh token has expired"
#         )
    
#     return user


