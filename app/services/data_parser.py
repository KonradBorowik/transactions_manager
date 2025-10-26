from fastapi import UploadFile
import logging
from pydantic import ValidationError

from app.schemas.transaction_schema import Transaction
from app.models.transaction_model import TransactionModel


class DataParserService:
    def parse_line(self, line: str, line_no: int) -> Transaction:
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
                transaction = Transaction.model_validate(content_dict)
                logging.info(f"Successfully parsed line {line_no}")
                return transaction
            else:
                logging.warning(f"[Line {line_no}] Expected 7 items, got {len(items)}")
                return None

        except ValidationError as e:
            logging.error(f"[Line {line_no}] Data validation failed: {str(e)}")
            return None

    def parse_file(self, file: UploadFile) -> list[Transaction]:
        transactions: list[Transaction] = []
        error_count = 0
        success_count = 0
        failed_lines: list[int] = []

        for line_no, line in enumerate(file.file.readlines()):
            line: str = line.decode("utf-8").rstrip("\n")
            transaction = self.parse_line(line=line.strip("\\n"), line_no=line_no)
            if transaction:
                transactions.append(transaction)
                success_count += 1
            else:
                failed_lines.append(line_no)
                error_count += 1

        logging.info(f"File parsing completed. Successful: {success_count}, Failed: {error_count}")
        if error_count:
            logging.info(f"Falied lines: {failed_lines}")
            
        return transactions

    def convert_to_pydantic(self, tr_models: list[TransactionModel]) -> list[Transaction]:
        transactions: Transaction = []
        for tr_model in tr_models:
            transactions.append(Transaction.model_validate(tr_model))

        return transactions
