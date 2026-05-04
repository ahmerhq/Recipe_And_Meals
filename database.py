from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os 
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DB_URL")
engine = create_engine(db_url)

sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()




