from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from auth import auth_handler, oauth
from models import user 
from schemas import user as user_schema
from database import engine, get_db


router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post("/signup/", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserView)
async def create_user(user_input: user_schema.UserSignUp, db: Session = Depends(get_db)):

    try:
        hashed_password = auth_handler.hash(user_input.password)
        user_input.password= hashed_password
        new_user = user.UserModel(**user_input.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as e:
        print(f"some error occured while creating user:{e._message}")
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"user with email, {user_input.email} already exists.")
    
    return new_user

@router.get("/profile/{id}", status_code=status.HTTP_200_OK, response_model=user_schema.UserView)
async def get_user(id, db: Session = Depends(get_db), current_user = Depends(oauth.get_current_user) ):

    res_user = db.query(user.UserModel).filter(user.UserModel.id == id).first()
    if not res_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} doesn't exist")
           
    return current_user