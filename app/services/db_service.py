from sqlalchemy.orm import Session
from typing import Union
from uuid import UUID

from app.db.database import (
    get_all_from_db,
    get_queried_from_db,
    store_in_db,
    get_amount,
    get_item_occurrences,
    get_latest_timestamp,
    get_unique_count
)
from app.schemas.transaction_schema import Transaction
from app.models.transaction_model import TransactionModel


class DatabaseService:
    def __init__(self, db: Session):
        self.db = db
        self.currency_rates = {
            "EUR": 4.3,
            "USD": 4.0,
            "PLN": 1.0
        }
        
    def store_data(self, data: list[Transaction]) -> None:
        for tr in data:
            tr_model = TransactionModel(**tr.model_dump())
            store_in_db(db=self.db, tr_model=tr_model)
                    

    def get_data(
        self,
        filters: Union[dict[str, str], None] = None,
        skip: int = -1,
        limit: int = -1) -> list[TransactionModel]:
        if filters:
            return get_queried_from_db(
                db=self.db,
                filters=filters,
                skip=skip,
                limit=limit
            )
        else:
            return get_all_from_db(
                db=self.db,
                skip=skip,
                limit=limit
            )


    def currency_conversion(self, income: dict) -> float:
        total = 0
        for currency, amount in income:
            rate = self.currency_rates.get(currency, 0)
            total += amount * rate
        return total


    def get_product_summary(self, product_id: UUID) -> dict:
        income_unconverted = get_amount(db=self.db, field_name="product_id", field_id=product_id)
        print(income_unconverted)
        sold_count = get_item_occurrences(db=self.db, item_id=product_id)
        unique_clients = get_unique_count(
            db=self.db,
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
        income_unconverted = get_amount(db=self.db, field_name="customer_id", field_id=customer_id)
        unique_products = get_unique_count(
            db=self.db,
            field_name="customer_id",
            field_id=customer_id,
            entry_to_count="product_id"
        )
        last_timestamp = get_latest_timestamp(db=self.db, field_name="customer_id", filter_id=customer_id)
        
        return {
            "total income": self.currency_conversion(income=income_unconverted),
            "unique products count": unique_products,
            "last transaction": last_timestamp
        }
