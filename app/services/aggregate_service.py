from datetime import datetime
from uuid import UUID

from app.schemas.transaction_schema import Transaction


EUR_PLN_RATE = 4.3
USD_PLN_RATE = 4


def currency_conversion(amount: float, currency: str) -> float:
    if currency == "EUR":
        return amount * EUR_PLN_RATE
    if currency == "USD":
        return amount * USD_PLN_RATE
    return amount


def add_unique_product(product_id: UUID, unique_items: list[UUID]) -> list[UUID]:
    if product_id not in unique_items:
        unique_items.append(product_id)

    return unique_items


def check_if_last_timestamp(ts: datetime, last_ts: datetime) -> datetime:
    if ts > last_ts:
        return ts
    return last_ts


def get_client_summary(transactions: list[Transaction]) -> dict:
    total_spendings = 0
    unique_items: list[UUID] = []
    last_timestamp: datetime = None
    for tr in transactions:
        total_spendings += currency_conversion(amount=tr.amount, currency=tr.currency)
        unique_items = add_unique_product(product_id=tr.product_id, unique_items=unique_items)
        last_timestamp = check_if_last_timestamp(ts=tr.timestamp, last_ts=last_timestamp)

    return {
        "total_spendings": total_spendings,
        "unique_items_count": len(unique_items),
        "last_transaction": last_timestamp
    }


def get_product_summary(transactions: Transaction) -> dict:
    total_spendings = 0
    unique_items: list[UUID] = []
    last_timestamp: datetime = None
    for tr in transactions:
        total_spendings += currency_conversion(amount=tr.amount, currency=tr.currency)
        unique_items = add_unique_product(product_id=tr.product_id, unique_items=unique_items)
        last_timestamp = check_if_last_timestamp(ts=tr.timestamp, last_ts=last_timestamp)

    return {
        "total_spendings": total_spendings,
        "unique_items_count": len(unique_items),
        "last_transaction": last_timestamp
    }