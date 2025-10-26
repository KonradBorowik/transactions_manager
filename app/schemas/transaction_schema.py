from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from uuid import UUID


class Currency(str, Enum):
    PLN = "PLN"
    EUR = "EUR"
    USD = "USD"


class Transaction(BaseModel):
    transaction_id: UUID
    timestamp: datetime
    amount: float
    currency: Currency
    customer_id: UUID
    product_id: UUID
    quantity: int

    class Config:
        from_attributes = True
