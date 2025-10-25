from fastapi import FastAPI

from app.api import (
    get_transactions,
    upload_csv,
)
from app.db.session import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(upload_csv.router, prefix="/api", tags=["Upload CSV"])
app.include_router(get_transactions.router, prefix="/api", tags=["Get Transactions"])

