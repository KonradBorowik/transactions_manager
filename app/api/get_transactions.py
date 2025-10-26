from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session
from typing import Union
from uuid import UUID

from app.db.database_operations import get_db
from app.services.data_parser import DataParserService
from app.services.db_service import DatabaseService


router = APIRouter()


def _create_filter(c_id: Union[str, None], p_id: Union[str, None]) -> dict:
    filters = {}
    if c_id:
        filters["customer_id"] = c_id
    if p_id:
        filters["product_id"] = p_id

    return filters


@router.get("/")
def get_transactions(
    skip: int = 0,
    limit: int = 20,
    customer_id: str = "",
    product_id: str = "",
    db: Session = Depends(get_db)
):
    filters = _create_filter(c_id=customer_id, p_id=product_id)
    
    db_service = DatabaseService(db=db)
    tr_models = db_service.get_data(filters=filters, skip=skip, limit=limit)
    data_parser = DataParserService()
    transactions = data_parser.convert_to_pydantic(tr_models=tr_models)
    
    if transactions:
        return [tr.model_dump() for tr in transactions]
    else:
        return {"No entries found."}


@router.get("/{transaction_id}")
def get_transaction_by_id(transaction_id: UUID, db: Session = Depends(get_db)):
    db_service = DatabaseService(db=db)
    tr_models = db_service.get_data(filters={"transaction_id": transaction_id})
    data_parser = DataParserService()
    transactions = data_parser.convert_to_pydantic(tr_models=tr_models)

    if transactions:
        return transactions[0]
    else:
        return {f"No transaction with the id: {transaction_id} found."}
