from fastapi import FastAPI

from routers import user as user_router, auth as auth_router, plan as plan_router
from models import user, plan
from database import engine, get_db

import stripe


user.Base.metadata.create_all(bind=engine) 
plan.Base.metadata.create_all(bind=engine) 

app = FastAPI()

app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(plan_router.router)

@app.get("/")
def home():
    return {"message": "Welcome to app"}

@app.post("/process-payment/")
async def process_payment(amount: int, currency: str, token: str):
    try:
        # Create a charge using the Stripe API
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source=token,  # Stripe token obtained from the client-side (e.g., Stripe.js)
            description="Payment made for subscription plan",  # Add a description for the payment
        )

        # You can handle the charge object as per your requirements
        # For example, log the payment or perform other actions

        # Return a success response
        return {"status": "success", "charge_id": charge.id}

    except stripe.error.CardError as e:
        # Handle specific Stripe errors
        return {"status": "error", "message": str(e)}
    except stripe.error.StripeError as e:
        # Handle generic Stripe errors
        return {"status": "error", "message": "Something went wrong. Please try again later."}