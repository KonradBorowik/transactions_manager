from fastapi import FastAPI

from app.api import upload_csv
from app.db.session import engine, Base
# from app.models.transaction import Transaction

app = FastAPI()
app.include_router(upload_csv.router, prefix="/api", tags=["Upload CSV"])

# Base.metadata.create_all(bind=engine)
