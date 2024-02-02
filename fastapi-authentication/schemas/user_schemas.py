from pydantic import BaseModel,EmailStr,constr



# class UserSchema(BaseModel):
#     email: EmailStr
#     password: constr(
#         min_length=8,
#         max_length=20
#     )

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None