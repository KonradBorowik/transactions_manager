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


def store_data(db: Session, data: list[Transaction]) -> None:
    for tr in data:
        tr_model = TransactionModel(**tr.model_dump())
        store_in_db(db=db, tr_model=tr_model)
                

def get_data(
    db: Session,
    filters: Union[dict[str, str], None] = None,
    skip: int = -1,
    limit: int = -1) -> list[TransactionModel]:
    if filters:
        tr_models: list[TransactionModel] = get_queried_from_db(
            db=db,
            filters=filters,
            skip=skip,
            limit=limit
        )
    else:
        tr_models: list[TransactionModel] = get_all_from_db(
            db=db,
            skip=skip,
            limit=limit
        )

    return tr_models


def currency_conversion(income: dict) -> float:
    total = 0
    for sum in income:
        if sum[0] == "EUR":
            total += sum[1] * 4.3
        if sum[0] == "USD":
            total += sum[1] * 4.0
        if sum[0] == "PLN":
            total += sum[1]

    return total


def get_product_summary(
    db: Session,
    product_id: UUID) -> list[TransactionModel]:
    income_unconverted = get_amount(db=db, field_name="product_id", field_id=product_id)
    print(income_unconverted)
    sold_count = get_item_occurrences(db=db, item_id=product_id)
    unique_clients = get_unique_count(
        db=db,
        field_name="product_id",
        field_id=product_id,
        entry_to_count="customer_id"
    )

    return {
        "items sold": sold_count,
        "total income": currency_conversion(income=income_unconverted),
        "unique clients": unique_clients
    }


def get_client_summary(db: Session, customer_id: UUID) -> dict:
    income_unconverted = get_amount(db=db, field_name="customer_id", field_id=customer_id)
    unique_products = get_unique_count(
        db=db,
        field_name="customer_id",
        field_id=customer_id,
        entry_to_count="product_id"
    )
    last_timestamp = get_latest_timestamp(db=db, field_name="customer_id", filter_id=customer_id)
    
    return {
        "total income": currency_conversion(income=income_unconverted),
        "unique products count": unique_products,
        "last transaction": last_timestamp
    }
