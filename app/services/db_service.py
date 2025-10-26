from sqlalchemy.orm import Session
from typing import Union
from uuid import UUID

from app.db.database_operations import DatabaseOperations
from app.schemas.transaction_schema import Transaction
from app.models.transaction_model import TransactionModel


class DatabaseService:
    def __init__(self, db: Session):
        self.db_ops = DatabaseOperations(db=db)
        self.currency_rates = {
            "EUR": 4.3,
            "USD": 4.0,
            "PLN": 1.0
        }
        
    def store_data(self, data: list[Transaction]) -> None:
        for tr in data:
            tr_model = TransactionModel(**tr.model_dump())
            self.db_ops.store(tr_model=tr_model)

    def get_data(
        self,
        filters: Union[dict[str, str], None] = None,
        skip: int = -1,
        limit: int = -1) -> list[TransactionModel]:
        if filters:
            return self.db_ops.get_filtered(filters=filters, skip=skip, limit=limit)
        return self.db_ops.get_all(skip=skip, limit=limit)

    def currency_conversion(self, income: dict) -> float:
        total = 0
        for currency, amount in income:
            rate = self.currency_rates.get(currency, 0)
            total += amount * rate
        return total

    def get_product_summary(self, product_id: UUID) -> dict:
        income_unconverted = self.db_ops.get_amount_summary(field_name="product_id", field_id=product_id)
        print(income_unconverted)
        sold_count = self.db_ops.get_item_count(item_id=product_id)
        unique_clients = self.db_ops.get_unique_count(
            field_name="product_id",
            field_id=product_id,
            entry_to_count="customer_id"
        )

        return {
            "items sold": sold_count,
            "total income": self.currency_conversion(income=income_unconverted),
            "unique clients": unique_clients
        }

    def get_client_summary(self, customer_id: UUID) -> dict:
        income_unconverted = self.db_ops.get_amount_summary(field_name="customer_id", field_id=customer_id)
        unique_products = self.db_ops.get_unique_count(
            field_name="customer_id",
            field_id=customer_id,
            entry_to_count="product_id"
        )
        last_timestamp = self.db_ops.get_latest_timestamp(field_name="customer_id", filter_id=customer_id)
        
        return {
            "total income": self.currency_conversion(income=income_unconverted),
            "unique products count": unique_products,
            "last transaction": last_timestamp
        }
