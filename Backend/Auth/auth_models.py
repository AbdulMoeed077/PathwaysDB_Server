from pydantic import BaseModel, EmailStr
from pydantic import Field
import re

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    email: EmailStr
    fname: str = Field(max_length=35)
    lname: str = Field(max_length=35)

class User(UserBase):
    id: str 
    is_active: bool = False

class UserCreate(User):
    password: str

class UserRoles(UserCreate):
    roles: list[str] = []


    class Config:
        from_attributes = True

def validate_password(password: str) -> bool:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return bool(re.match(pattern, password))

# Password gr3at@3wdsG
# Example usage
password = "StrongP@ss123"
if not validate_password(password):
    print("Password does not meet the criteria.")
else:
    print("Password is valid.")