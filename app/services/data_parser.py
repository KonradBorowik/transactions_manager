from fastapi import UploadFile
from pydantic import ValidationError
from typing import Union

from app.schemas.transaction_schema import Transaction


class DataParser:
    def _parse_line(self, line: str, line_no: int) -> Transaction:
        try:
            items = [item.strip() for item in line.split(',') if item.strip()]
            if len(items) == 7:
                content_dict = {
                    "transaction_id": items[0],
                    "timestamp": items[1],
                    "amount": items[2],
                    "currency": items[3],
                    "customer_id": items[4],
                    "product_id": items[5],
                    "quantity": items[6],
                }
                return Transaction.model_validate(content_dict)
            else:
                print(f"[Line {line_no}] Expected 7 items, got {len(items)}.")

        except ValidationError:
            print(f"[Line {line_no}] Data validation failed.")

    def parse_file(self, file: UploadFile) -> list[Transaction]:
        transactions: list[Transaction] = []
        for line_no, line in enumerate(file.file.readlines()):
            line: str = line.decode("utf-8").rstrip("\n")
            transaction = self._parse_line(line=line.strip("\\n"), line_no=line_no)
            if transaction:
                transactions.append(transaction)
        
        return transactions
