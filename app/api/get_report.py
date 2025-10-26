from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database_operations import get_db
from app.services.db_service import DatabaseService

router = APIRouter()


@router.get("/customer-summary/{customer_id}")
def get_customer_report(customer_id: UUID, db: Session = Depends(get_db)):
    db_service = DatabaseService(db=db)
    summary = db_service.get_client_summary(customer_id=customer_id)
    if summary:
        return summary
    return {"message": "Customer id not found."}


@router.get("/product-summary/{product_id}")
def get_product_report(product_id: UUID, db: Session = Depends(get_db)):
    db_service = DatabaseService(db=db)
    summary = db_service.get_product_summary(product_id=product_id)
    
    if summary:
        return summary
    return {"message": "Product id not found"}