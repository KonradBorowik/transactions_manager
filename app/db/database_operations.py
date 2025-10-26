from datetime import datetime
import logging
from sqlalchemy import (
    and_,
    func,
    distinct,
    select
)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Union, Optional
from uuid import UUID

from app.models.transaction_model import TransactionModel
from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DatabaseOperations:
    def __init__(self, db: Session):
        self.db = db

    def store(self, tr_model: TransactionModel) -> None:
        try:
            self.db.add(tr_model)
            self.db.commit()
            self.db.refresh(tr_model)
        except IntegrityError:
            self.db.rollback()
            print("Row already exists in the database.")

    def get_all(
        self,
        skip: int,
        limit: int) -> list[TransactionModel]:
        try:
            result = self.db.query(TransactionModel).offset(skip).limit(limit).all()
            logging.info(f"Retrieved {len(result)} transactions")
            return result
        except SQLAlchemyError as e:
            logging.error(f"Error retrieving transactions: {str(e)}")
            return []

    def get_filtered(
        self,
        filters: dict[str, str],
        skip: int,
        limit: int) -> list[TransactionModel]:
        try: 
            conditions = []
            for key, value in filters.items():
                column = getattr(TransactionModel, key)
                if column:
                    conditions.append(column == value)
                else:
                    logging.warning(f"Invalid filter field: {key}")

            if skip > -1 and limit > -1:
                query = select(TransactionModel).where(and_(*conditions)).offset(skip).limit(limit)
            else:
                query = select(TransactionModel).where(and_(*conditions))
            
            result = self.db.execute(query).scalars().all()
            logging.info(f"Retrieved {len(result)} filtered transactions")
            return result
        except SQLAlchemyError as e:
            logging.error(f"Error retrieving filtered transactions: {str(e)}")
            return []

    def get_amount_summary(self, field_name: str, field_id: UUID) -> dict:
        try:
            query = select(
                TransactionModel.currency,
                func.sum(TransactionModel.amount).label("total_amount")
            ).where(
                getattr(TransactionModel, field_name) == field_id
            ).group_by(TransactionModel.currency)

            result = self.db.execute(query).all()
            logging.info(f"Retrieved amount summary for {field_name}: {field_id}")
            return result
        except SQLAlchemyError as e:
            logging.error(f"Error getting amount summary: {str(e)}")
            return []

    def get_unique_count(self, field_name: str, field_id: UUID, entry_to_count: str) -> int:
        try:
            query = (
                select(func.count(distinct(getattr(TransactionModel, entry_to_count))))
                .where(getattr(TransactionModel, field_name) == field_id)
            )

            result = self.db.execute(query).scalar() or 0
            logging.info(f"Retrieved unique count for {entry_to_count}")
            return result
        except SQLAlchemyError as e:
            logging.error(f"Error getting unique count: {str(e)}")
            return 0

    def get_item_count(self, item_id: UUID) -> int:
        try:
            query = select(func.count()).where(TransactionModel.product_id == item_id)
            result = self.db.execute(query).scalar() or 0
            logging.info(f"Retrieved item count for product: {item_id}")
            return result
        except SQLAlchemyError as e:
            logging.error(f"Error getting item count: {str(e)}")
            return 0        

    def get_latest_timestamp(self, field_name: str, filter_id: UUID) -> datetime:
        try:
            query = (
                select(func.max(TransactionModel.timestamp))
                .where(getattr(TransactionModel, field_name) == filter_id)
            )

            result = self.db.execute(query).scalar()
            logging.info(f"Retrieved latest timestamp for {field_name}: {filter_id}")
            return result
        except SQLAlchemyError as e:
            logging.error(f"Error getting latest timestamp: {str(e)}")
            return None
