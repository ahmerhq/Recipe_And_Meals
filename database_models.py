from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)
    auth_provider= Column(String, default="local")
    created_at = Column(DateTime, default=datetime.utcnow)
    favorite_meal = Column(String, nullable=True)
    google_access_token = Column(String, nullable=True)
    google_refresh_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    refresh_token_expiry = Column(DateTime, nullable=True)

    recipe_table = relationship("Recipe", back_populates="assigned_user", cascade="all, delete-orphan")

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String)
    item_country = Column(String)
    item_category = Column(String)
    item_recipe = Column(String)


    # imported from top
    user_id = Column(Integer, ForeignKey("users.id"))
    assigned_user = relationship("User", back_populates="recipe_table")


