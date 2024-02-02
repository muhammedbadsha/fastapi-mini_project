from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt, JWTError
from decouple import config
from schemas import CreateUserRequest,Token

router = APIRouter(
    prefix='/users',
    tags=['auth']   
    )

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
becrypt_context = CryptContext(schemes=['bcrypt'],deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
db_dependancy = Annotated[Session, Depends(get_db)]

@router.post('/',status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependancy, create_user_request: CreateUserRequest):
    username = create_user_request.email.split('@')[0]
    create_user_model = Users(
        username=username,
        email= create_user_request.email,
        hashed_password = becrypt_context.hash(create_user_request.password),
    )
    db.add(create_user_model)
    db.commit()

@router.post("/token",response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependancy):
    user = authenticate_user(form_data.username,form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = create_access_token(form_data.username, user.id, timedelta(minutes=30))
    return {"access_token":token, 'token_type':'bearer'}

def authenticate_user(username : str, password : str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not becrypt_context.verify(password,user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id : int, expires_delta: timedelta):
    encode = {'sub':username, 'id':user_id}
    expires = datetime.utcnow()+expires_delta
    encode.update({'exp':expires})        
    return jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM)

async def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        username : str = payload.get('sub')
        user_id:int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="could not validate user")
        return {'username':username, 'id':user_id }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')