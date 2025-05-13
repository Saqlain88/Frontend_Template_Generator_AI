from pydantic import BaseModel
from typing import ClassVar

class PlanSchema(BaseModel):
    plan_name : str
    credits_per_month : int
    price_per_month : float
    