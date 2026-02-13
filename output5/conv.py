from datetime import date, datetime

class Transaction:
    def __init__(self, transaction_id, customer_id, amount, currency, transaction_date, region):
        self.transaction_id = transaction_id
        self.customer_id = customer_id
        self.amount = amount
        self.currency = currency
        self.transaction_date = transaction_date
        self.region = region

    def get_transaction_id(self):
        return self.transaction_id

    def get_customer_id(self):
        return self.customer_id

    def get_amount(self):
        return self.amount

    def get_currency(self):
        return self.currency

    def get_transaction_date(self):
        return self.transaction_date

    def get_region(self):
        return self.region


class RawRecord:
    def __init__(self, raw_line):
        self.raw_line = raw_line


class TransactionValidator:
    def is_valid(self, tx):
        if tx.get_transaction_id() is None or tx.get_transaction_id() == "":
            return False

        if tx.get_customer_id() is None or tx.get_customer_id() == "":
            return False

        if tx.get_amount() <= 0:
            return False

        if tx.get_transaction_date() > date.today():
            return False

        return True


class TransactionTransformer:
    FX_RATES = {
        "USD": 1.0,
        "INR": 0.012,
        "EUR": 1.1
    }

    def normalize_currency(self, tx):
        rate = self.FX_RATES.get(tx.get_currency(), 1.0)
        normalized_amount = tx.get_amount() * rate
        return Transaction(
            tx.get_transaction_id(),
            tx.get_customer_id(),
            normalized_amount,
            "USD",
            tx.get_transaction_date(),
            tx.get_region()
        )


class MetricsAggregator:
    def total_amount_by_region(self, transactions):
        totals = {}
        for tx in transactions:
            region = tx.get_region()
            totals[region] = totals.get(region, 0.0) + tx.get_amount()
        return totals


class ErrorSink:
    def __init__(self):
        self.bad_records = []

    def record_error(self, raw_record, reason):
        self.bad_records.append(f"{raw_record} | ERROR: {reason}")

    def get_bad_records(self):
        return self.bad_records


class OutputSink:
    def write_metrics(self, metrics):
        print("=== Aggregated Metrics ===")
        for region, total in metrics.items():
            print(f"Region: {region}, Total Amount (USD): {total}")


class DataPipeline:
    def __init__(self):
        self.validator = TransactionValidator()
        self.transformer = TransactionTransformer()
        self.aggregator = MetricsAggregator()
        self.error_sink = ErrorSink()
        self.output_sink = OutputSink()

    def run(self, raw_records):
        valid_transactions = []
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

    def parse(self, line):
        parts = line.split(",")
        return Transaction(
            parts[0],
            parts[1],
            float(parts[2]),
            parts[3],
            datetime.strptime(parts[4], "%Y-%m-%d").date(),
            parts[5]
        )


if __name__ == "__main__":
    input_records = [
        RawRecord("TXN1,CUST1,1000,USD,2024-01-10,US"),
        RawRecord("TXN2,CUST2,5000,INR,2024-01-11,INDIA"),
        RawRecord("TXN3,CUST3,-200,EUR,2024-01-12,EU"),
        RawRecord("TXN4,CUST4,800,EUR,2030-01-01,EU")
    ]

    pipeline = DataPipeline()
    pipeline.run(input_records)
