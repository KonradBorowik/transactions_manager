from fastapi import (
    APIRouter,
    Depends,
    UploadFile
)
import logging
from sqlalchemy.orm import Session

from app.db.database_operations import get_db
from app.services.data_parser import DataParserService
from app.services.db_service import DatabaseService


router = APIRouter()


@router.post("/upload")
async def upload_csv(uploaded_file: UploadFile, db: Session = Depends(get_db)):
    logging.info(f"Processing {uploaded_file}.")
    if uploaded_file.filename.endswith(".csv"):
        data_parser = DataParserService()
        transactions = data_parser.parse_file(file=uploaded_file)
        
        db_service = DatabaseService(db=db)
        db_service.store_data(data=transactions)

        logging.info(f"{uploaded_file} processed successfully.")
        return {"Upload successful!"}
    else:
        logging.info(f"Could not process file {uploaded_file}.")
        return {"error": "Only CSV files are allowed."}
