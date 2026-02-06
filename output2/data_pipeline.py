"""
Data Pipeline: Python Implementation
Converted from Java for production use.
Python 3.10+ | Author: Senior Code Conversion and Refactoring Agent

Modules:
- Transaction: Data model
- RawRecord: Simulated input
- TransactionValidator: Validation logic
- TransactionTransformer: Currency normalization
- MetricsAggregator: Aggregation by region
- ErrorSink: Collection of bad records
- OutputSink: Metrics output
- DataPipeline: Orchestration
- Application: Runner

"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import datetime

# --- Data Model ---

@dataclass
class Transaction:
    """
    Represents a financial transaction.
    """
    transaction_id: str
    customer_id: str
    amount: float
    currency: str
    transaction_date: datetime.date
    region: str

# --- Raw Input Record ---

@dataclass
class RawRecord:
    """
    Simulates raw input record from file or Kafka.
    """
    raw_line: str

# --- Validator ---

class TransactionValidator:
    """
    Validates Transaction objects for required fields and logical correctness.
    """

    def is_valid(self, tx: Transaction) -> bool:
        if not tx.transaction_id or not tx.transaction_id.strip():
            return False
        if not tx.customer_id or not tx.customer_id.strip():
            return False
        if tx.amount <= 0:
            return False
        if tx.transaction_date > datetime.date.today():
            return False
        return True

# --- Transformer (Currency Normalization) ---

class TransactionTransformer:
    """
    Normalizes transaction amount to USD using predefined FX rates.
    """
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

# --- Aggregator (Metrics Calculation) ---

class MetricsAggregator:
    """
    Aggregates total transaction amounts by region.
    """

    def total_amount_by_region(self, transactions: List[Transaction]) -> Dict[str, float]:
        totals: Dict[str, float] = {}
        for tx in transactions:
            totals[tx.region] = totals.get(tx.region, 0.0) + tx.amount
        return totals

# --- Error Sink (Bad Records) ---

class ErrorSink:
    """
    Collects bad records and error reasons.
    """

    def __init__(self):
        self.bad_records: List[str] = []

    def record_error(self, raw_record: str, reason: str) -> None:
        self.bad_records.append(f"{raw_record} | ERROR: {reason}")

    def get_bad_records(self) -> List[str]:
        return self.bad_records

# --- Output Sink (Metrics Output) ---

class OutputSink:
    """
    Outputs aggregated metrics to console (simulates data lake/warehouse).
    """

    def write_metrics(self, metrics: Dict[str, float]) -> None:
        print("=== Aggregated Metrics ===")
        for region, total in metrics.items():
            print(f"Region: {region}, Total Amount (USD): {total}")

# --- Pipeline Orchestrator ---

class DataPipeline:
    """
    Orchestrates the data pipeline: parse, validate, transform, aggregate, and output.
    """

    def __init__(self):
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

        # Optionally, print bad records for audit
        if self.error_sink.get_bad_records():
            print("\n=== Error Records ===")
            for err in self.error_sink.get_bad_records():
                print(err)

    def parse(self, line: str) -> Transaction:
        """
        Parses a raw CSV line into a Transaction object.
        Expected format:
        transaction_id,customer_id,amount,currency,transaction_date,region
        """
        parts = line.strip().split(",")
        if len(parts) != 6:
            raise ValueError("Malformed input line (expected 6 fields)")
        transaction_id = parts[0]
        customer_id = parts[1]
        try:
            amount = float(parts[2])
        except ValueError:
            raise ValueError(f"Invalid amount: {parts[2]}")
        currency = parts[3]
        try:
            transaction_date = datetime.date.fromisoformat(parts[4])
        except ValueError:
            raise ValueError(f"Invalid date: {parts[4]}")
        region = parts[5]
        return Transaction(
            transaction_id=transaction_id,
            customer_id=customer_id,
            amount=amount,
            currency=currency,
            transaction_date=transaction_date,
            region=region,
        )

# --- Main Application (Pipeline Execution) ---

def main():
    """
    Entry point for the data pipeline application.
    """
    input_records = [
        RawRecord("TXN1,CUST1,1000,USD,2024-01-10,US"),
        RawRecord("TXN2,CUST2,5000,INR,2024-01-11,INDIA"),
        RawRecord("TXN3,CUST3,-200,EUR,2024-01-12,EU"),
        RawRecord("TXN4,CUST4,800,EUR,2030-01-01,EU"),
    ]

    pipeline = DataPipeline()
    pipeline.run(input_records)

if __name__ == "__main__":
    main()
