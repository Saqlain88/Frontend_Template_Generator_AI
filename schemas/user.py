from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignUp(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    is_admin: bool = False
    
class UserView(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    is_admin: bool = False
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class TokenModel(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None