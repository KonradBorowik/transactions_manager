from fastapi import (
    APIRouter,
    Depends,
    UploadFile
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.data_parser import parse_file
from app.services.db_service import store_data


router = APIRouter()

@router.post("/upload")
async def upload_csv(uploaded_file: UploadFile, db: Session = Depends(get_db)):
    if uploaded_file.filename.endswith(".csv"):
        transactions = parse_file(file=uploaded_file)
        store_data(db=db, data=transactions)

        return {"Upload successful!"}
    else:
        return {"error": "Only CSV files are allowed."}
