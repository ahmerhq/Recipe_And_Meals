from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from database_models import Base
from database import engine
from authentication import signup, login
import recipe
from oauth_google import router as google_auth_router

app = FastAPI(title="Recipe & Meals App")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000",  "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(signup.router)
app.include_router(login.router)
app.include_router(recipe.router)
app.include_router(google_auth_router)

# Serve static HTML files from the current directory (MUST be last!)
app.mount("/", StaticFiles(directory=str(Path(__file__).parent), html=True), name="static")









