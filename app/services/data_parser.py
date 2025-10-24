import io
from fastapi import UploadFile
from pydantic import ValidationError

from app.schemas.transaction import Transaction

class InvalidLineLength(Exception):
    pass

class DataParser:
    def __init__(self, uploaded_file: UploadFile) -> None:
        self.file = uploaded_file

    def _parse_line(self, line: str, line_no: int) -> Transaction:
        try:
            line_content = line.split(",")
            if len(line_content) == 7:
                content_dict = {
                    "transaction_id": line_content[0],
                    "timestamp": line_content[1],
                    "amount": line_content[2],
                    "currency": line_content[3],
                    "customer_id": line_content[4],
                    "product_id": line_content[5],
                    "quantity": line_content[6],
                }
                return Transaction.model_validate(content_dict)
            else:
                print(f"[Line {line_no}] Expected 7 items, got {len(line_content)}.")

        except ValidationError:
            print(f"[Line {line_no}] Data validation failed.")

    def parse_file(self) -> list[Transaction]:
        transactions: list[Transaction] = []
        for line_no, line in enumerate(self.file.file.readlines()):
            line: str = line.decode("utf-8").rstrip("\n")
            transactions.append(self._parse_line(line=line.strip("\\n"), line_no=line_no))
        
        return transactions
