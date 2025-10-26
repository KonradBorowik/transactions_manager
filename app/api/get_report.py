from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db
from app.services.db_service import get_data


router = APIRouter()


@router.get("/customer-summary/{customer_id}")
def get_customer_report(customer_id: UUID, db: Session = Depends(get_db)):
    transactions = get_data(db=db, filters={"customer_id": customer_id})
