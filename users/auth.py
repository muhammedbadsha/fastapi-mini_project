from jose import JWTError,jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends,HTTPException,status
from models.user_modes import UserDB
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user_schemas import TokenData
from typing import Annotated
from sqlalchemy.orm import Session
from decouple import config
SECRET_KEY = config('SECRET_KEY')

ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTE = config('ACCESS_TOKEN_EXPIRE_MINUTE')

bcry_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")



def verify_password(plain_password, hashed_password):
    return bcry_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return bcry_context.hash(password)


def get_user(db, username: str):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    print(user)
    if user is not None:
        # print(db)
        # user_data = db[username]
        return user
    return {"details":f'there has no user called {username}'}
    
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    print(user.password_hash)
    if user is None:
        print("user is worked false")
        return False
    password = verify_password(password, user.password_hash)
    if password is None:
        print('this worked false')
        return False

    return user
  
# def create_access_token(username: str, user_id : int, expires_delta: timedelta):
#     encode = {'sub':username, 'id':user_id}
#     expires = datetime.utcnow()+expires_delta
#     encode.update({'exp':expires})
#     return jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# def create_jwt_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail="Could not validate Credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credential_exception
        token_data = TokenData(email = username)
    except JWTError:
        raise credential_exception
    
    user = get_user(username = token_data.username)
    if user is None:
        raise credential_exception
    return user
