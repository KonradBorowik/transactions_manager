from fastapi import FastAPI

from app.api import (
    get_report,
    get_transactions,
    upload_csv,
)
from app.db.session import engine, Base


class TransactionManagerApp:
    def __init__(self):
        self.app = FastAPI()
        self._init_database()
        self._init_routes()

    def _init_database(self):
        Base.metadata.create_all(bind=engine)

    def _init_routes(self):
        self.app.include_router(
            upload_csv.router, 
            prefix="/transactions", 
            tags=["Upload CSV"]
        )
        self.app.include_router(
            get_transactions.router, 
            prefix="/transactions", 
            tags=["Get Transactions"]
        )
        self.app.include_router(
            get_report.router, 
            prefix="/reports", 
            tags=["Get Reports"]
        )

    def get_application(self) -> FastAPI:
        return self.app
    

app = TransactionManagerApp().get_application()
