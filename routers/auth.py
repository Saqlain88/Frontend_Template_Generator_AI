
from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from auth import auth_handler, oauth
from models import user 
from schemas import user as user_schema
from database import engine, get_db

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login/", response_model=user_schema.TokenModel)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    _user_ = db.query(user.UserModel).filter(user.UserModel.email == user_credentials.username).first()
    
    if not _user_:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not auth_handler.verif(user_credentials.password, _user_.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
        
    access_token = oauth.create_access_token(data={'user_id': _user_.id})
           
    return {"access_token":access_token, "token_type": "bearer"}
    