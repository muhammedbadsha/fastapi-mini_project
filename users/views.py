from fastapi import APIRouter
from database.msql import engine,Session
from datetime import datetime,timedelta
from jose import jwt,JWTError
from schemas.user_schemas import UserSchema
from models.user_modes import UserDB
from passlib.context import CryptContext
import os

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


router = APIRouter()

# JWT token creation function
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")
    return encoded_jwt

@router.get('/')
def get_valiue():
    return {'value':"default"}

# Endpoint to create a new user
@router.post("/users/", response_model=UserDB)
async def create_user(user: UserSchema):
    cursor = conn.cursor()
    hashed_password = CryptContext(schemes=["bcrypt"]).hash(user.password)
    new_user = UserDB(email=user.email, password=hashed_password)
    query = "INSERT INTO items (email, password) VALUES (%s, %s)"
    curser
    return new_user