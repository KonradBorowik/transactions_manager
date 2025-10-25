from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session
from typing import Union

from app.db.database import get_db
from app.services.db_service import get_data


router = APIRouter()


def _create_filter(c_id: Union[str, None], p_id: Union[str, None]) -> dict:
    filters = {}
    if c_id:
        filters["customer_id"] = c_id
    if p_id:
        filters["product_id"] = p_id

    return filters


@router.get("/transactions")
def get_transactions(skip: int = 0, limit:int = 20, customer_id: str = None, product_id: str = None, db: Session = Depends(get_db)):
    filters = _create_filter(c_id=customer_id, p_id=product_id)
    
    transactions = get_data(db=db, filters=filters, skip=skip, limit=limit)

    if transactions:
        return [tr.model_dump() for tr in transactions]
    else:
        return {"No entries found."}
