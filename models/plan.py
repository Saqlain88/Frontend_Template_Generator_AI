from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from database import Base

class PlanModel(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, nullable=False)
    plan_name = Column(String, nullable=False)
    credits_per_month = Column(Integer, nullable=False)
    price_per_month = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
     
