from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from datetime import datetime, timedelta



from models.user_modes import UserDB

def create_user(db: Session, email: str, password: str):
    # hashed_password = bcrypt.hash(password)
    username = email.split('@')[0]
    db_user = UserDB(email=email,username = username)
    db_user.set_password(password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


