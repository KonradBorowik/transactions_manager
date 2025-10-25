from sqlalchemy.orm import Session
from typing import Union

from app.db.database import (
    get_all_from_db,
    get_queried_from_db,
    store_in_db
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
    skip: int = 0,
    limit: int = 20) -> list[Transaction]:
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

    transactions: Transaction = []
    for tr_model in tr_models:
        transactions.append(Transaction.model_validate(tr_model))

    return transactions
