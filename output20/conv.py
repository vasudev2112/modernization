from datetime import date, datetime

class Transaction:
    def __init__(self, transactionId, customerId, amount, currency, transactionDate, region):
        self._transactionId = transactionId
        self._customerId = customerId
        self._amount = amount
        self._currency = currency
        self._transactionDate = transactionDate
        self._region = region

    def getTransactionId(self):
        return self._transactionId

    def getCustomerId(self):
        return self._customerId

    def getAmount(self):
        return self._amount

    def getCurrency(self):
        return self._currency

    def getTransactionDate(self):
        return self._transactionDate

    def getRegion(self):
        return self._region

class RawRecord:
    def __init__(self, rawLine):
        self.rawLine = rawLine

class TransactionValidator:
    def isValid(self, tx):
        if tx.getTransactionId() is None or tx.getTransactionId() == "":
            return False

        if tx.getCustomerId() is None or tx.getCustomerId() == "":
            return False

        if tx.getAmount() <= 0:
            return False

        if tx.getTransactionDate() > date.today():
            return False

        return True

class TransactionTransformer:
    FX_RATES = {
        "USD": 1.0,
        "INR": 0.012,
        "EUR": 1.1
    }

    def normalizeCurrency(self, tx):
        rate = self.FX_RATES.get(tx.getCurrency(), 1.0)
        normalizedAmount = tx.getAmount() * rate

        return Transaction(
            tx.getTransactionId(),
            tx.getCustomerId(),
            normalizedAmount,
            "USD",
            tx.getTransactionDate(),
            tx.getRegion()
        )

class MetricsAggregator:
    def totalAmountByRegion(self, transactions):
        totals = {}
        for tx in transactions:
            region = tx.getRegion()
            totals[region] = totals.get(region, 0.0) + tx.getAmount()
        return totals

class ErrorSink:
    def __init__(self):
        self.badRecords = []

    def recordError(self, rawRecord, reason):
        self.badRecords.append(rawRecord + " | ERROR: " + reason)

    def getBadRecords(self):
        return self.badRecords

class OutputSink:
    def writeMetrics(self, metrics):
        print("=== Aggregated Metrics ===")
        for region, total in metrics.items():
            print("Region: " + str(region) + ", Total Amount (USD): " + str(total))

class DataPipeline:
    def __init__(self):
        self.validator = TransactionValidator()
        self.transformer = TransactionTransformer()
        self.aggregator = MetricsAggregator()
        self.errorSink = ErrorSink()
        self.outputSink = OutputSink()

    def run(self, rawRecords):
        validTransactions = []

        for record in rawRecords:
            try:
                tx = self.parse(record.rawLine)

                if self.validator.isValid(tx):
                    normalized = self.transformer.normalizeCurrency(tx)
                    validTransactions.append(normalized)
                else:
                    self.errorSink.recordError(record.rawLine, "Validation failed")

            except Exception as e:
                self.errorSink.recordError(record.rawLine, str(e))

        metrics = self.aggregator.totalAmountByRegion(validTransactions)
        self.outputSink.writeMetrics(metrics)

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
    input = [
        RawRecord("TXN1,CUST1,1000,USD,2024-01-10,US"),
        RawRecord("TXN2,CUST2,5000,INR,2024-01-11,INDIA"),
        RawRecord("TXN3,CUST3,-200,EUR,2024-01-12,EU"),
        RawRecord("TXN4,CUST4,800,EUR,2030-01-01,EU")
    ]

    pipeline = DataPipeline()
    pipeline.run(input)
