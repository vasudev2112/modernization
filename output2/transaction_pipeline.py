from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Dict

@dataclass
class Transaction:
    transaction_id: str
    customer_id: str
    amount: float
    currency: str
    transaction_date: date
    region: str

@dataclass
class RawRecord:
    raw_line: str

class TransactionValidator:
    def is_valid(self, tx: Transaction) -> bool:
        if not tx.transaction_id:
            return False
        if not tx.customer_id:
            return False
        if tx.amount <= 0:
            return False
        if tx.transaction_date > date.today():
            return False
        return True

class TransactionTransformer:
    FX_RATES: Dict[str, float] = {
        "USD": 1.0,
        "INR": 0.012,
        "EUR": 1.1,
    }
    def normalize_currency(self, tx: Transaction) -> Transaction:
        rate = self.FX_RATES.get(tx.currency, 1.0)
        normalized_amount = tx.amount * rate
        return Transaction(
            transaction_id=tx.transaction_id,
            customer_id=tx.customer_id,
            amount=normalized_amount,
            currency="USD",
            transaction_date=tx.transaction_date,
            region=tx.region,
        )

class MetricsAggregator:
    def total_amount_by_region(self, transactions: List[Transaction]) -> Dict[str, float]:
        totals: Dict[str, float] = {}
        for tx in transactions:
            totals[tx.region] = totals.get(tx.region, 0.0) + tx.amount
        return totals

class ErrorSink:
    def __init__(self) -> None:
        self.bad_records: List[str] = []
    def record_error(self, raw_record: str, reason: str) -> None:
        self.bad_records.append(f"{raw_record} | ERROR: {reason}")
    def get_bad_records(self) -> List[str]:
        return self.bad_records

class OutputSink:
    def write_metrics(self, metrics: Dict[str, float]) -> None:
        print("=== Aggregated Metrics ===")
        for region, total in metrics.items():
            print(f"Region: {region}, Total Amount (USD): {total}")

class DataPipeline:
    def __init__(self) -> None:
        self.validator = TransactionValidator()
        self.transformer = TransactionTransformer()
        self.aggregator = MetricsAggregator()
        self.error_sink = ErrorSink()
        self.output_sink = OutputSink()
    def run(self, raw_records: List[RawRecord]) -> None:
        valid_transactions: List[Transaction] = []
        for record in raw_records:
            try:
                tx = self.parse(record.raw_line)
                if self.validator.is_valid(tx):
                    normalized = self.transformer.normalize_currency(tx)
                    valid_transactions.append(normalized)
                else:
                    self.error_sink.record_error(record.raw_line, "Validation failed")
            except Exception as e:
                self.error_sink.record_error(record.raw_line, str(e))
        metrics = self.aggregator.total_amount_by_region(valid_transactions)
        self.output_sink.write_metrics(metrics)
        if self.error_sink.get_bad_records():
            print("\n=== Bad Records ===")
            for err in self.error_sink.get_bad_records():
                print(err)
    def parse(self, line: str) -> Transaction:
        parts = line.strip().split(",")
        if len(parts) != 6:
            raise ValueError("Incorrect number of fields")
        transaction_id, customer_id, amount_str, currency, date_str, region = parts
        try:
            amount = float(amount_str)
        except ValueError:
            raise ValueError("Invalid amount")
        try:
            tx_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format")
        return Transaction(
            transaction_id=transaction_id,
            customer_id=customer_id,
            amount=amount,
            currency=currency,
            transaction_date=tx_date,
            region=region
        )

if __name__ == "__main__":
    input_records = [
        RawRecord("TXN1,CUST1,1000,USD,2024-01-10,US"),
        RawRecord("TXN2,CUST2,5000,INR,2024-01-11,INDIA"),
        RawRecord("TXN3,CUST3,-200,EUR,2024-01-12,EU"),
        RawRecord("TXN4,CUST4,800,EUR,2030-01-01,EU"),
    ]
    pipeline = DataPipeline()
    pipeline.run(input_records)
