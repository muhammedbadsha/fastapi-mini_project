from fastapi import FastAPI,status,Depends,HTTPException,APIRouter
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session



app = FastAPI()


app.include_router()

router = APIRouter(prefix='/users')
models.Base.metadata.create_all(bind= engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]

