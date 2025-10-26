from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.db_service import get_data


router = APIRouter()


@router.get("/customer-summary/{customer_id}")
def get_customer_report(db: Session = Depends(get_db)):
    pass