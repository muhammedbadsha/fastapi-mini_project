from fastapi import FastAPI,status,Depends,HTTPException,APIRouter
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from auth import router,get_current_user


app = FastAPI()


app.include_router(router)


models.Base.metadata.create_all(bind= engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[Session, Depends(get_current_user)]
