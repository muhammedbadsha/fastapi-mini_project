from pydantic import BaseModel,EmailStr,constr



class UserSchema(BaseModel):
    email: EmailStr
    password: constr(
        min_length=8,
        max_length=20
    )