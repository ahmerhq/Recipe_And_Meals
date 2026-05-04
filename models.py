from pydantic import BaseModel, EmailStr, field_validator
import re
from datetime import datetime
from typing import Optional

class userCreate(BaseModel):
    email: EmailStr
    username: str
    password: Optional[str] = None   # allow None for Google users
    auth_provider: str = "local"     # default is local

    #setting email 
    @field_validator("email")
    def check_email(cls, v:str)->str:
        pattern = r'^[a-zA-Z0-9]+\.?[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+$'
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v
    
    # setting password requirements
    @field_validator("password")
    def check_password(cls, p, values):
        # Only enforce password if local signup
        if values.get("auth_provider") == "local":
            if not p or len(p) < 2:
                raise ValueError("Password must be at least 2 characters long")
        return p

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    auth_provider: str 
    created_at: datetime

    class config:
        from_attributes=True


class userCredentials(BaseModel):
    email:EmailStr
  

class itemByNameCreate(BaseModel):  
    item:str

class itemByNameResponse(BaseModel):
    item_name:str
    item_country:str
    item_category:str
    item_recipe:str
    
class UserFavFood(BaseModel):
    favorite_food:str

class UserFavResponse(BaseModel):
    id:int
    item_name:str
    item_country:str
    item_category:str
    item_recipe:str   
    user_id:int


class token(BaseModel):
    access_token:str
    token_type: str


class token_data(BaseModel):
    id: Optional[int] = None
