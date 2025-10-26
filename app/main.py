from fastapi import FastAPI
import logging

from app.api import (
    get_report,
    get_transactions,
    upload_csv,
)
from app.db.session import engine, Base


class TransactionManagerApp:
    def __init__(self):
        self._init_logging()
        logging.info("Initializing Application...")
        self.app = FastAPI()
        self._init_database()
        self._init_routes()
        logging.info("Application initialized successfully!")

    def _init_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

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
