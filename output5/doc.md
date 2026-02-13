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

- Method Name: Transaction (constructor)
  - Parameters: String transactionId, String customerId, double amount, String currency, LocalDate transactionDate, String region
  - Return Type: (none, constructor)
  - Description: Initializes a Transaction object with the provided transaction details.

- Method Name: getTransactionId
  - Parameters: none
  - Return Type: String
  - Description: Returns the transaction ID.

- Method Name: getCustomerId
  - Parameters: none
  - Return Type: String
  - Description: Returns the customer ID.

- Method Name: getAmount
  - Parameters: none
  - Return Type: double
  - Description: Returns the transaction amount.

- Method Name: getCurrency
  - Parameters: none
  - Return Type: String
  - Description: Returns the currency of the transaction.

- Method Name: getTransactionDate
  - Parameters: none
  - Return Type: LocalDate
  - Description: Returns the date of the transaction.

- Method Name: getRegion
  - Parameters: none
  - Return Type: String
  - Description: Returns the region of the transaction.

---

### Class: RawRecord

#### Methods

- Method Name: RawRecord (constructor)
  - Parameters: String rawLine
  - Return Type: (none, constructor)
  - Description: Initializes a RawRecord object with the provided raw line.

---

### Class: TransactionValidator

#### Methods

- Method Name: isValid
  - Parameters: Transaction tx
  - Return Type: boolean
  - Description: Checks if a Transaction object is valid based on several criteria (non-null fields, positive amount, date not in the future).

---

### Class: TransactionTransformer

#### Methods

- Method Name: normalizeCurrency
  - Parameters: Transaction tx
  - Return Type: Transaction
  - Description: Converts the transaction amount to USD using predefined exchange rates and returns a new Transaction object.

---

### Class: MetricsAggregator

#### Methods

- Method Name: totalAmountByRegion
  - Parameters: List<Transaction> transactions
  - Return Type: Map<String, Double>
  - Description: Aggregates the total transaction amount by region.

---

### Class: ErrorSink

#### Methods

- Method Name: recordError
  - Parameters: String rawRecord, String reason
  - Return Type: void
  - Description: Records an error message for a raw record.

- Method Name: getBadRecords
  - Parameters: none
  - Return Type: List<String>
  - Description: Returns the list of bad records.

---

### Class: OutputSink

#### Methods

- Method Name: writeMetrics
  - Parameters: Map<String, Double> metrics
  - Return Type: void
  - Description: Outputs aggregated metrics to the console.

---

### Class: DataPipeline

#### Methods

- Method Name: run
  - Parameters: List<RawRecord> rawRecords
  - Return Type: void
  - Description: Processes a list of raw records, parses them, validates transactions, normalizes currency, aggregates metrics, handles errors, and outputs results.

- Method Name: parse
  - Parameters: String line
  - Return Type: Transaction
  - Description: Parses a comma-separated line into a Transaction object.

---

### Class: Application

#### Methods

- Method Name: main
  - Parameters: String[] args
  - Return Type: void
  - Description: Entry point. Creates sample raw records, initializes DataPipeline, and runs the pipeline.

## 4. Exception Handling

- The DataPipeline class handles exceptions during parsing and processing of raw records in the run method. If an exception occurs, it records the error message with the associated raw record using ErrorSink.

## 5. Execution Flow

- The Application class's main method creates a list of RawRecord objects with sample data.
- It creates an instance of DataPipeline and calls its run method with the input list.
- The DataPipeline parses each raw line into a Transaction, validates it, normalizes the currency, aggregates metrics by region, records errors for invalid or malformed records, and outputs the aggregated metrics.

## 6. Observations

- All classes are defined in the same file.
- The code uses basic Java standard library classes for collections, dates, and console output.
- Currency normalization is hardcoded with specific exchange rates for USD, INR, and EUR.
- Errors are collected and accessible via ErrorSink but are not output in the main flow.
- The pipeline expects the input in a specific CSV format.

## 7. Static Analysis Limitations

- Behavior not determinable from static code analysis: The actual output to the console, error handling in edge cases, and the completeness of validation logic cannot be fully assessed without runtime execution.
- No package declarations or visibility modifiers are specified, so all classes have default/package-private visibility.
- The code's thread safety, performance, and integration with external systems cannot be determined from the static code alone.

----------