from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Transaction(BaseModel):
    __tablename__ = "transactions"
    transaction_id: UUID
    timestamp: datetime
    amount: float
    currency: str
    customer_id: UUID
    product_id: UUID
    quantity: int
