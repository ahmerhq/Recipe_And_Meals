from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database_models import Base
from database import engine
from authentication import signup, login
import recipe


app = FastAPI(title="Recipe & Meals App")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(signup.router)
app.include_router(login.router)
app.include_router(recipe.router)




@app.get("/")
def Greetings():
    return {"message": "Hello User. Hope you're all set to see some quality dishes."}









