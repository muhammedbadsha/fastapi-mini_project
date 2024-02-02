from database.msql import Base,engine
from sqlalchemy import Column,Integer, String,DateTime
from datetime import datetime
from passlib.hash import bcrypt


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    password_hash = Column(String(300))  # Store the hashed password

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

Base.metadata.create_all(bind=engine)