from sqlalchemy import (
    and_,
    select
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Union

from app.models.transaction_model import TransactionModel
from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def store_in_db(db: Session, tr_model: TransactionModel) -> None:
    try:
        db.add(tr_model)
        db.commit()
        db.refresh(tr_model)
    except IntegrityError:
        db.rollback()
        print("Row already exists in the database.")


def get_all_from_db(
    db: Session,
    skip: int,
    limit: int) -> Union[list[TransactionModel], None]:
    return db.query(TransactionModel).offset(skip).limit(limit).all()


def get_queried_from_db(
    db: Session,
    filters: dict[str, str],
    skip: int,
    limit: int) -> Union[list[TransactionModel], None]:
    conditions = []
    for key, value in filters.items():
        column = getattr(TransactionModel, key)
        if column:
            conditions.append(column == value)
    if skip > -1 and limit > -1:
        query = select(TransactionModel).where(and_(*conditions)).offset(skip).limit(limit)
    else:
        query = select(TransactionModel).where(and_(*conditions))
    return db.execute(query).scalars().all()
