from fastapi import APIRouter, Depends, HTTPException,status
from database.msql import engine,Session
from datetime import datetime,timedelta
from jose import jwt,JWTError
# from schemas.user_schemas import UserSchema
from models.user_modes import UserDB
from passlib.context import CryptContext
from sqlalchemy.orm import Session,sessionmaker
from schemas.user_schemas import UserCreate,Token
from users.crud import create_user
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from users.auth import authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTE, bcry_context,oauth2_scheme,SECRET_KEY,ALGORITHM

# from fastapi.exceptions import 
import os

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependancy = Annotated[Session,Depends(get_db)]

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

# JWT token creation function
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")
#     return encoded_jwt

@router.get('/')
def get_valiue():
    return {'value':"default"}


class UserCreateRequest(UserCreate):
    pass
# Endpoint to create a new user
@router.post("/users/")
def register(user_create: UserCreateRequest, db: Session = Depends(get_db)):
    db_user = create_user(db, email=user_create.email, password=user_create.password)
    return {
        "user": {
            "id": db_user.id,
            "email": db_user.email,
        }
    }

# @router.get('/users/')
# async def get_user(user: UserSchema) -> UserSchema:
#     return {'user': 'none'}

@router.post('/token', response_model=Token)
@router.post("/token")
async def login_for_access_token(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user or not bcry_context.verify(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(f'{email}, {password}')
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTE))
    access_token = create_access_token(data={"sub": email}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    print("this worked")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
    except JWTError as e:
        print(f'jwtError: {e}')
        raise credentials_exception
    return {'email': email}

@router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    print("atleast this worked")
    return current_user