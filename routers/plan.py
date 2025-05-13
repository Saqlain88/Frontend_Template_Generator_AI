from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from auth import oauth
from models import plan
from schemas import plan as plan_schema
from database import engine, get_db

router = APIRouter(
    prefix="/plan",
    tags=["Plans"]
)

@router.get("/", response_model=List[plan_schema.PlanSchema])
def get_plans(db: Session = Depends(get_db)):
    plans = db.query(plan.PlanModel).all()
    return plans

@router.get("/{id}", response_model=plan_schema.PlanSchema)
def get_plan(id: int, db: Session = Depends(get_db)):
    res_plan = db.query(plan.PlanModel).filter( plan.PlanModel.id == id ).first()
    if not res_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Plan with id: {id} doesn't exist")
    return res_plan

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=plan_schema.PlanSchema)
def create_plan(plan_input: plan_schema.PlanSchema , db: Session = Depends(get_db), current_user: Session = Depends(oauth.get_current_user)):
    new_plan = plan.PlanModel(**plan_input.dict())
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan