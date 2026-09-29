import os
import stripe
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Charity Match Backend")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class DonationRequest(BaseModel):
    amount: int  # amount in cents (e.g., 1000 = $10.00)
    currency: str = "usd"
    charity_name: str

@app.get("/")
def read_root():
    return {"status": "Backend running"}

@app.post("/create-donation-intent")
def create_donation_intent(donation: DonationRequest):
    try:
        # Create a PaymentIntent with matching metadata
        intent = stripe.PaymentIntent.create(
            amount=donation.amount,
            currency=donation.currency,
            metadata={"charity": donation.charity_name, "match_eligible": "true"},
            automatic_payment_methods={"enabled": True},
        )
        return {"clientSecret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
