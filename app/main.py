from fastapi import FastAPI

from app.api import (
    get_report,
    get_transactions,
    upload_csv,
)
from app.db.session import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(upload_csv.router, prefix="/transactions", tags=["Upload CSV"])
app.include_router(get_transactions.router, prefix="/transactions", tags=["Get Transactions"])
app.include_router(get_report.router, prefix="/reports", tags=["Get Reports"])
