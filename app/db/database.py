from datetime import datetime
from sqlalchemy import (
    and_,
    func,
    distinct,
    select
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Union
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
        limit: int) -> Union[list[TransactionModel], None]:
        return self.db.query(TransactionModel).offset(skip).limit(limit).all()

    def get_filtered(
        self,
        filters: dict[str, str],
        skip: int,
        limit: int) -> list[TransactionModel]:
        conditions = []
        for key, value in filters.items():
            column = getattr(TransactionModel, key)
            if column:
                conditions.append(column == value)

        if skip > -1 and limit > -1:
            query = select(TransactionModel).where(and_(*conditions)).offset(skip).limit(limit)
        else:
            query = select(TransactionModel).where(and_(*conditions))
        
        return self.db.execute(query).scalars().all()


    def get_amount_summary(self, field_name: str, field_id: UUID) -> dict:
        query = select(
            TransactionModel.currency,
            func.sum(TransactionModel.amount).label("total_amount")
        ).where(
            getattr(TransactionModel, field_name) == field_id
        ).group_by(TransactionModel.currency)

        return self.db.execute(query).all()


    def get_unique_count(self, field_name: str, field_id: UUID, entry_to_count: str) -> int:
        query = (
            select(func.count(distinct(getattr(TransactionModel, entry_to_count))))
            .where(getattr(TransactionModel, field_name) == field_id)
        )

        return self.db.execute(query).scalar()


    def get_item_count(self, item_id: UUID) -> int:
        query = select(func.count()).where(TransactionModel.product_id == item_id)
        
        return self.db.execute(query).scalar()


    def get_latest_timestamp(self, field_name: str, filter_id: UUID) -> datetime:
        query = (
            select(func.max(TransactionModel.timestamp))
            .where(getattr(TransactionModel, field_name) == filter_id)
        )

        return self.db.execute(query).scalar()
