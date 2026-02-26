# Code Documentation

## 1. File Overview

- File Name: pipeline_java.txt

- Language: Java

- Location: input1/pipeline_java.txt

## 2. Imports

- java.time.LocalDate
- java.util.HashMap
- java.util.Map
- java.util.List
- java.util.ArrayList
- java.util.Arrays

## 3. Classes

### Class: Transaction

#### Methods

- Constructor: Transaction(String transactionId, String customerId, double amount, String currency, LocalDate transactionDate, String region)
  - Parameters: String transactionId, String customerId, double amount, String currency, LocalDate transactionDate, String region
  - Return Type: (constructor, no return type)
  - Description: Initializes a Transaction object with transactionId, customerId, amount, currency, transactionDate, and region.

- Method Name: getTransactionId()
  - Parameters: None
  - Return Type: String
  - Description: Returns the transaction ID.

- Method Name: getCustomerId()
  - Parameters: None
  - Return Type: String
  - Description: Returns the customer ID.

- Method Name: getAmount()
  - Parameters: None
  - Return Type: double
  - Description: Returns the transaction amount.

- Method Name: getCurrency()
  - Parameters: None
  - Return Type: String
  - Description: Returns the currency.

- Method Name: getTransactionDate()
  - Parameters: None
  - Return Type: LocalDate
  - Description: Returns the transaction date.

- Method Name: getRegion()
  - Parameters: None
  - Return Type: String
  - Description: Returns the region.


### Class: RawRecord

#### Methods

- Constructor: RawRecord(String rawLine)
  - Parameters: String rawLine
  - Return Type: (constructor, no return type)
  - Description: Initializes a RawRecord with a raw input line.


### Class: TransactionValidator

#### Methods

- Method Name: isValid(Transaction tx)
  - Parameters: Transaction tx
  - Return Type: boolean
  - Description: Validates a Transaction object. Returns true if transactionId and customerId are not null or empty, amount is greater than 0, and transactionDate is not in the future; otherwise, returns false.


### Class: TransactionTransformer

#### Methods

- Method Name: normalizeCurrency(Transaction tx)
  - Parameters: Transaction tx
  - Return Type: Transaction
  - Description: Converts the transaction amount to USD using predefined FX rates and returns a new Transaction object with the normalized amount.


### Class: MetricsAggregator

#### Methods

- Method Name: totalAmountByRegion(List<Transaction> transactions)
  - Parameters: List<Transaction> transactions
  - Return Type: Map<String, Double>
  - Description: Aggregates total transaction amounts by region and returns a map of region to total amount.


### Class: ErrorSink

#### Methods

- Method Name: recordError(String rawRecord, String reason)
  - Parameters: String rawRecord, String reason
  - Return Type: void
  - Description: Records an error message with the raw record and the specified reason.

- Method Name: getBadRecords()
  - Parameters: None
  - Return Type: List<String>
  - Description: Returns the list of bad records.


### Class: OutputSink

#### Methods

- Method Name: writeMetrics(Map<String, Double> metrics)
  - Parameters: Map<String, Double> metrics
  - Return Type: void
  - Description: Outputs aggregated metrics to the console.


### Class: DataPipeline

#### Methods

- Method Name: run(List<RawRecord> rawRecords)
  - Parameters: List<RawRecord> rawRecords
  - Return Type: void
  - Description: Processes a list of raw records, parses each to a Transaction, validates and normalizes them, aggregates metrics, and writes the output. Errors are recorded.

- Method Name: parse(String line)
  - Parameters: String line
  - Return Type: Transaction
  - Description: Parses a comma-separated line into a Transaction object.


### Class: Application

#### Methods

- Method Name: main(String[] args)
  - Parameters: String[] args
  - Return Type: void
  - Description: Entry point. Creates sample RawRecord data, initializes DataPipeline, and runs the pipeline.

## 4. Exception Handling

- In DataPipeline.run, the parsing of each raw record is wrapped in a try-catch block. If an exception occurs during parsing or validation, the error is recorded using ErrorSink.recordError with the exception message.

## 5. Execution Flow

- The Application class's main method constructs a list of RawRecord objects with sample data.
- It creates a DataPipeline instance and calls the run method.
- DataPipeline.run parses, validates, and normalizes transactions, aggregates metrics by region, and outputs the results.
- Errors encountered during parsing or validation are recorded.

## 6. Observations

- FX rates for currency normalization are hard-coded in TransactionTransformer.
- Error records are collected but only output via ErrorSink's getBadRecords method, not printed in the main flow.
- All output is printed to the console by OutputSink.

## 7. Static Analysis Limitations

- No information on thread safety or concurrency.
- No details about input/output beyond console printing and in-memory lists.
- Actual business logic or intent is not determinable beyond code structure.
- Behavior for malformed input lines is not specified beyond error recording.
- No external configuration, persistence, or integration is visible from the code.

----------
