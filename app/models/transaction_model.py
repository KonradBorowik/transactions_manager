from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    UUID
)
from app.db.session import Base


class TransactionModel(Base):
    __tablename__ = "transactions"
    transaction_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    customer_id = Column(UUID(as_uuid=True), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    quantity = Column(Integer, nullable=False)
