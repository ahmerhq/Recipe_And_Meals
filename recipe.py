import requests
from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import JSONResponse
from models import itemByNameCreate, itemByNameResponse, UserFavFood, UserFavResponse
from database import get_db
from sqlalchemy.orm import Session
from database_models import User, Recipe
from oauth2 import allow_access


router = APIRouter(tags=["Recipe & Meals"])

# search item by name
@router.post("/recipe", response_model=itemByNameResponse)
def item_by_name(name:itemByNameCreate):
    Recipe_URL = "https://www.themealdb.com/api/json/v1/1/search.php"
    payload = {"s": name}

    response = requests.get(Recipe_URL, params=payload)
    data = response.json()

    if not data["meals"]:
        raise HTTPException(status_code=404, detail="Unavailable item for recipe.")

    recipe = itemByNameResponse(
        item_name=data["meals"][0]["strMeal"],
        item_country=data["meals"][0]["strArea"],
        item_category=data["meals"][0]["strCategory"],
        item_recipe=data["meals"][0]["strInstructions"].replace("\r\n", "<br>"),
    )
    return recipe


# Random Meal
@router.get("/recipe/random", response_model=itemByNameResponse)
def random_recipe():
    random_url = "https://www.themealdb.com/api/json/v1/1/random.php"
    response = requests.get(random_url)
    data = response.json()

    recipe = itemByNameResponse(
        item_name=data["meals"][0]["strMeal"],
        item_country=data["meals"][0]["strArea"],
        item_category=data["meals"][0]["strCategory"],
        item_recipe=data["meals"][0]["strInstructions"].replace("\r\n", "<br>"),
    )
    return recipe
    


# Filter by category
@router.post("/recipe/filter/{category}")
def check_item_by_category(category:str):
    filter_by_category = "https://www.themealdb.com/api/json/v1/1/filter.php"
    payload = {"c": category}

    response = requests.get(filter_by_category, params=payload)
    data = response.json()

    if not data["meals"]:
        raise HTTPException(status_code=404, detail="Invalid category. Use like 'seafood', 'veegtarian'")
    lis = []

    for i in data["meals"]:
        lis.append(i["strMeal"])
    
    return lis


# Filter by country
@router.post("/recipe/{country}")
def check_item_by_country(country:str):
    filter_by_country_url = "https://www.themealdb.com/api/json/v1/1/filter.php"
    payload = {"a": country}

    response = requests.get(filter_by_country_url, params=payload)
    data = response.json()

    if not data["meals"]:
        raise HTTPException(status_code=404, detail="Country not supported or uneven name. Use like 'Canadian', 'American'")
    new_list = []

    for i in data["meals"]:
        new_list.append(i["strMeal"])
    return new_list


# ask user for his fav food and add in database.
@router.post("/favorite_meal")
def add_fav(favorite_meal:UserFavFood, db:Session = Depends(get_db),uc:User = Depends(allow_access)):
    user_fav = db.query(User).filter(User.id == uc.id).first()

    # search via users given fav meal exist in db or not
    url = "https://www.themealdb.com/api/json/v1/1/search.php"
    payload = {"s": favorite_meal.favorite_food}

    response = requests.get(url, params=payload)
    data = response.json()

    if not data["meals"]:
        raise HTTPException(status_code=404, detail="Unavailable item for recipe. Cannot set as favorite meal.")

    user_fav.favorite_meal = data["meals"][0]["strMeal"]
    db.commit()
    db.refresh(user_fav)
    return {"message": f"{favorite_meal.favorite_food} has been set as your favorite meal."}


# Give user ingredient and all of his defaulted fav food
@router.get("/recipe/favorite", response_model=UserFavResponse)
def recipe_of_fav_item(db:Session = Depends(get_db), uc:User = Depends(allow_access)):
    db_user = db.query(User).filter(User.id == uc.id).first()

    url = "https://www.themealdb.com/api/json/v1/1/search.php"
    payload = {"s": db_user.favorite_meal}

    response = requests.get(url, params=payload)
    data = response.json()

    # Ensure meals is a list
    if not data.get("meals") or not isinstance(data["meals"], list):
        raise HTTPException(status_code=404, detail="Favorite meal not found. Please set a valid favorite meal.")
    
    meal = data["meals"][0]

    recipe = Recipe(
        item_name=meal.get("strMeal", "Unknown"),
        item_country=meal.get("strArea", "Unknown"),
        item_category=meal.get("strCategory", "Unknown"),
        item_recipe=meal.get("strInstructions", "").replace("\r\n", "\n"),
        user_id=db_user.id
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


# delete user 
@router.delete("/delete")
def delete_account(response: Response,  db:Session = Depends(get_db),uc:User = Depends(allow_access)):
    db_user = db.query(User).filter(User.id == uc.id).first()

    db.delete(db_user)
    db.commit()

    response.delete_cookie("refresh_token")
    response.status_code = 200
    return JSONResponse(content={"message": "Your account and all related data has been deleted"}) 










