from fastapi import (
    APIRouter,
    UploadFile
)

from app.services import DataParser


router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(uploaded_file: UploadFile):
    if uploaded_file.filename.endswith(".csv"):
        data_parser = DataParser(uploaded_file=uploaded_file)
        transactions = data_parser.parse_file()
        
        

        return {"Upload successful!"}
    else:
        return {"error": "Only CSV files are allowed."}
