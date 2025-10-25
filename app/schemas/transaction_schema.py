from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Transaction(BaseModel):
    transaction_id: UUID
    timestamp: datetime
    amount: float
    currency: str
    customer_id: UUID
    product_id: UUID
    quantity: int

    class Config:
        from_attributes = True
