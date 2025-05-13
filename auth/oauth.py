from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import database
from sqlalchemy.orm import Session

from schemas import user as user_schema
from models import user as user_model

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")


# SECRET_KEY
# Alogorithm
# exp time

# use below to generate a strong and random string for your secret key
# openssl rand -hex 32   

SECRET_KEY = "3ec03fc1a1bc1c007a6c791f804ba1cd2256011c72b5d2861e12ccb21c063af1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
                                            
        id : str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        
        token_data = user_schema.TokenData(id=id)        
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    
    curr_user = db.query(user_model.UserModel).filter(user_model.UserModel.id == token.id).first()
    
    
    return curr_user
    