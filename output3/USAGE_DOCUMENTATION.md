# DiscountCalculator - Usage Documentation

## Overview

The `DiscountCalculator` module provides a simple yet powerful way to calculate discounts based on customer type and purchase amount. This Python implementation has been converted from Java while maintaining full functional equivalence and adding modern Python enhancements.

---

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [API Reference](#api-reference)
4. [Usage Examples](#usage-examples)
5. [Business Rules](#business-rules)
6. [Advanced Usage](#advanced-usage)
7. [Error Handling](#error-handling)
8. [Performance Considerations](#performance-considerations)
9. [FAQ](#faq)

---

## Installation

### Requirements
- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

### Setup

1. **Download the module**:
   ```bash
   git clone https://github.com/vasudev2112/modernization.git
   cd modernization/output3
   ```

2. **Verify Python version**:
   ```bash
   python --version
   # Should show Python 3.6 or higher
   ```

3. **Run the module**:
   ```bash
   python discount_calculator.py
   ```

---

## Quick Start

### Basic Usage

```python
from discount_calculator import DiscountCalculator

# Calculate discount for a premium customer
final_amount = DiscountCalculator.calculate_discount(5000, "PREMIUM")
print(f"Final amount: ${final_amount}")  # Output: Final amount: $4000.0

# Calculate discount for a standard customer
final_amount = DiscountCalculator.calculate_discount(15000, "STANDARD")
print(f"Final amount: ${final_amount}")  # Output: Final amount: $12750.0
```

### Running as a Script

```bash
python discount_calculator.py
```

Output:
```
4000.0
12750.0
2000.0
```

---

## API Reference

### Class: `DiscountCalculator`

A utility class for calculating discounts based on customer type and purchase amount.

#### Constants

- **`PREMIUM`** (str): Constant for premium customer type ("PREMIUM")
- **`STANDARD`** (str): Constant for standard customer type ("STANDARD")

#### Methods

##### `calculate_discount(amount: float, customer_type: str) -> float`

Calculates the final amount after applying applicable discounts.

**Parameters:**
- `amount` (float): The original purchase amount before discounts
- `customer_type` (str): The type of customer (case-insensitive)
  - "PREMIUM": Premium customers (20% base discount)
  - "STANDARD": Standard customers (10% base discount)
  - Any other value: No customer-based discount

**Returns:**
- `float`: The final amount after applying all applicable discounts

**Discount Rules:**
1. Premium customers receive 20% discount
2. Standard customers receive 10% discount
3. Purchases over $10,000 receive an additional 5% discount
4. Final amount cannot be negative (minimum 0)

**Examples:**

```python
# Premium customer with $5,000 purchase
DiscountCalculator.calculate_discount(5000, "PREMIUM")
# Returns: 4000.0 (20% discount = $1,000 off)

# Standard customer with $15,000 purchase
DiscountCalculator.calculate_discount(15000, "STANDARD")
# Returns: 12750.0 (15% total discount = $2,250 off)

# Unknown customer type with $2,000 purchase
DiscountCalculator.calculate_discount(2000, "UNKNOWN")
# Returns: 2000.0 (no discount applied)
```

---

## Usage Examples

### Example 1: Basic Discount Calculation

```python
from discount_calculator import DiscountCalculator

# Premium customer purchases
amount = 5000
customer_type = "PREMIUM"
final = DiscountCalculator.calculate_discount(amount, customer_type)

print(f"Original Amount: ${amount}")
print(f"Customer Type: {customer_type}")
print(f"Final Amount: ${final}")
print(f"Savings: ${amount - final}")
```

Output:
```
Original Amount: $5000
Customer Type: PREMIUM
Final Amount: $4000.0
Savings: $1000.0
```

### Example 2: High-Value Purchase with Additional Discount

```python
from discount_calculator import DiscountCalculator

# Standard customer with high-value purchase
amount = 15000
customer_type = "STANDARD"
final = DiscountCalculator.calculate_discount(amount, customer_type)

# Calculate discount breakdown
base_discount = 0.10  # 10% for standard
additional_discount = 0.05  # 5% for high-value
total_discount = base_discount + additional_discount

print(f"Original Amount: ${amount}")
print(f"Base Discount (Standard): {base_discount * 100}%")
print(f"Additional Discount (High-Value): {additional_discount * 100}%")
print(f"Total Discount: {total_discount * 100}%")
print(f"Final Amount: ${final}")
print(f"Total Savings: ${amount - final}")
```

Output:
```
Original Amount: $15000
Base Discount (Standard): 10.0%
Additional Discount (High-Value): 5.0%
Total Discount: 15.0%
Final Amount: $12750.0
Total Savings: $2250.0
```

### Example 3: Batch Processing Multiple Customers

```python
from discount_calculator import DiscountCalculator

# Process multiple customer purchases
customers = [
    {"name": "Alice", "amount": 5000, "type": "PREMIUM"},
    {"name": "Bob", "amount": 15000, "type": "STANDARD"},
    {"name": "Charlie", "amount": 2000, "type": "STANDARD"},
    {"name": "Diana", "amount": 20000, "type": "PREMIUM"},
]

print("Customer Discount Report")
print("=" * 70)
print(f"{'Name':<10} {'Type':<10} {'Original':<12} {'Final':<12} {'Savings':<12}")
print("-" * 70)

total_original = 0
total_final = 0

for customer in customers:
    final = DiscountCalculator.calculate_discount(
        customer["amount"], 
        customer["type"]
    )
    savings = customer["amount"] - final
    
    print(f"{customer['name']:<10} {customer['type']:<10} "
          f"${customer['amount']:<11.2f} ${final:<11.2f} ${savings:<11.2f}")
    
    total_original += customer["amount"]
    total_final += final

print("-" * 70)
print(f"{'TOTAL':<10} {'':<10} ${total_original:<11.2f} "
      f"${total_final:<11.2f} ${total_original - total_final:<11.2f}")
print("=" * 70)
```

Output:
```
Customer Discount Report
======================================================================
Name       Type       Original     Final        Savings     
----------------------------------------------------------------------
Alice      PREMIUM    $5000.00     $4000.00     $1000.00    
Bob        STANDARD   $15000.00    $12750.00    $2250.00    
Charlie    STANDARD   $2000.00     $1800.00     $200.00     
Diana      PREMIUM    $20000.00    $15000.00    $5000.00    
----------------------------------------------------------------------
TOTAL                 $42000.00    $33550.00    $8450.00    
======================================================================
```

### Example 4: Case-Insensitive Customer Type

```python
from discount_calculator import DiscountCalculator

# All these are equivalent
result1 = DiscountCalculator.calculate_discount(5000, "PREMIUM")
result2 = DiscountCalculator.calculate_discount(5000, "premium")
result3 = DiscountCalculator.calculate_discount(5000, "Premium")
result4 = DiscountCalculator.calculate_discount(5000, "PrEmIuM")

print(f"All results are equal: {result1 == result2 == result3 == result4}")
# Output: All results are equal: True
```

### Example 5: Using Class Constants

```python
from discount_calculator import DiscountCalculator

# Use class constants for type safety
amount = 5000
final = DiscountCalculator.calculate_discount(
    amount, 
    DiscountCalculator.PREMIUM
)

print(f"Final amount for {DiscountCalculator.PREMIUM} customer: ${final}")
# Output: Final amount for PREMIUM customer: $4000.0
```

---

## Business Rules

### Discount Structure

#### Customer-Based Discounts

| Customer Type | Base Discount | Eligibility |
|---------------|---------------|-------------|
| PREMIUM       | 20%           | All premium customers |
| STANDARD      | 10%           | All standard customers |
| Other/Unknown | 0%            | No customer-based discount |

#### Purchase-Based Discounts

| Purchase Amount | Additional Discount | Combined with Customer Discount |
|-----------------|---------------------|----------------------------------|
| ≤ $10,000       | 0%                  | No                               |
| > $10,000       | 5%                  | Yes (additive)                   |

### Discount Calculation Formula

```
Total Discount = Customer Discount + (High-Value Discount if applicable)
Final Amount = Original Amount × (1 - Total Discount)
Final Amount = max(Final Amount, 0)  # Cannot be negative
```

### Examples of Discount Combinations

1. **Premium Customer, $5,000 Purchase**:
   - Customer Discount: 20%
   - High-Value Discount: 0% (amount ≤ $10,000)
   - Total Discount: 20%
   - Final: $5,000 × 0.80 = $4,000

2. **Premium Customer, $15,000 Purchase**:
   - Customer Discount: 20%
   - High-Value Discount: 5% (amount > $10,000)
   - Total Discount: 25%
   - Final: $15,000 × 0.75 = $11,250

3. **Standard Customer, $15,000 Purchase**:
   - Customer Discount: 10%
   - High-Value Discount: 5% (amount > $10,000)
   - Total Discount: 15%
   - Final: $15,000 × 0.85 = $12,750

4. **Unknown Customer, $2,000 Purchase**:
   - Customer Discount: 0%
   - High-Value Discount: 0% (amount ≤ $10,000)
   - Total Discount: 0%
   - Final: $2,000 × 1.00 = $2,000

---

## Advanced Usage

### Integration with Web Applications

```python
from flask import Flask, request, jsonify
from discount_calculator import DiscountCalculator

app = Flask(__name__)

@app.route('/calculate-discount', methods=['POST'])
def calculate_discount_api():
    data = request.json
    amount = float(data.get('amount', 0))
    customer_type = data.get('customer_type', '')
    
    final_amount = DiscountCalculator.calculate_discount(amount, customer_type)
    savings = amount - final_amount
    
    return jsonify({
        'original_amount': amount,
        'customer_type': customer_type,
        'final_amount': final_amount,
        'savings': savings,
        'discount_percentage': (savings / amount * 100) if amount > 0 else 0
    })

if __name__ == '__main__':
    app.run(debug=True)
```

### Custom Wrapper with Validation

```python
from discount_calculator import DiscountCalculator
from typing import Union

class EnhancedDiscountCalculator:
    """Enhanced wrapper with input validation and detailed reporting."""
    
    @staticmethod
    def calculate_with_validation(
        amount: Union[int, float], 
        customer_type: str
    ) -> dict:
        """Calculate discount with input validation and detailed breakdown."""
        
        # Validate inputs
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a number")
        
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        
        if not isinstance(customer_type, str):
            raise TypeError("Customer type must be a string")
        
        # Calculate discount
        final_amount = DiscountCalculator.calculate_discount(amount, customer_type)
        savings = amount - final_amount
        discount_percentage = (savings / amount * 100) if amount > 0 else 0
        
        # Determine discount breakdown
        customer_discount = 0
        if customer_type.upper() == "PREMIUM":
            customer_discount = 20
        elif customer_type.upper() == "STANDARD":
            customer_discount = 10
        
        high_value_discount = 5 if amount > 10000 else 0
        
        return {
            'original_amount': amount,
            'final_amount': final_amount,
            'total_savings': savings,
            'discount_percentage': discount_percentage,
            'breakdown': {
                'customer_discount': customer_discount,
                'high_value_discount': high_value_discount,
                'total_discount': customer_discount + high_value_discount
            },
            'customer_type': customer_type.upper()
        }

# Usage
result = EnhancedDiscountCalculator.calculate_with_validation(15000, "PREMIUM")
print(result)
```

---

## Error Handling

### Input Validation

While the current implementation is lenient, you may want to add validation:

```python
def safe_calculate_discount(amount, customer_type):
    """Wrapper with error handling."""
    try:
        # Validate amount
        if not isinstance(amount, (int, float)):
            return {"error": "Amount must be a number"}
        
        if amount < 0:
            return {"error": "Amount cannot be negative"}
        
        # Calculate discount
        final = DiscountCalculator.calculate_discount(amount, customer_type)
        
        return {
            "success": True,
            "original_amount": amount,
            "final_amount": final,
            "savings": amount - final
        }
    
    except Exception as e:
        return {"error": f"Calculation failed: {str(e)}"}

# Usage
result = safe_calculate_discount(5000, "PREMIUM")
if "error" in result:
    print(f"Error: {result['error']}")
else:
    print(f"Success: Final amount is ${result['final_amount']}")
```

---

## Performance Considerations

### Efficiency
- **Time Complexity**: O(1) - constant time for all operations
- **Space Complexity**: O(1) - no additional memory allocation
- **Thread Safety**: Yes - static method with no shared state

### Optimization Tips

1. **Batch Processing**: Process multiple calculations in parallel
   ```python
   from concurrent.futures import ThreadPoolExecutor
   
   def process_batch(customers):
       with ThreadPoolExecutor() as executor:
           results = executor.map(
               lambda c: DiscountCalculator.calculate_discount(c['amount'], c['type']),
               customers
           )
       return list(results)
   ```

2. **Caching**: For repeated calculations with same inputs
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def cached_calculate(amount, customer_type):
       return DiscountCalculator.calculate_discount(amount, customer_type)
   ```

---

## FAQ

### Q1: Can I use decimal amounts?
**A:** Yes, the calculator accepts any float value including decimals.
```python
DiscountCalculator.calculate_discount(1234.56, "PREMIUM")  # Works fine
```

### Q2: What happens if I pass an invalid customer type?
**A:** Invalid types are treated as unknown customers with 0% customer discount. High-value discount still applies if applicable.
```python
DiscountCalculator.calculate_discount(15000, "INVALID")  # Returns 14250.0 (5% discount only)
```

### Q3: Is the customer type case-sensitive?
**A:** No, the comparison is case-insensitive.
```python
DiscountCalculator.calculate_discount(5000, "premium")  # Same as "PREMIUM"
```

### Q4: Can the final amount be negative?
**A:** No, there's protection against negative amounts. Minimum is 0.
```python
DiscountCalculator.calculate_discount(100, "PREMIUM")  # Returns 80.0, not negative
```

### Q5: How do I add new customer types?
**A:** Modify the `calculate_discount` method to include new types:
```python
if customer_type.upper() == "VIP":
    discount = 0.30  # 30% for VIP customers
```

### Q6: Can I customize discount rates?
**A:** Yes, you can create a subclass or wrapper:
```python
class CustomDiscountCalculator(DiscountCalculator):
    DISCOUNT_RATES = {
        "PREMIUM": 0.25,  # Custom rate
        "STANDARD": 0.15,
        "VIP": 0.30
    }
```

---

## Support and Contribution

### Getting Help
- Review this documentation
- Check the migration report for technical details
- Review test cases for usage examples

### Reporting Issues
If you encounter any issues:
1. Check the troubleshooting guide in MIGRATION_REPORT.md
2. Verify your Python version (3.6+)
3. Ensure correct input types and values

### Best Practices
1. Always validate inputs before calling the calculator
2. Use class constants for customer types
3. Handle edge cases (zero amounts, very large amounts)
4. Add logging for production use
5. Write unit tests for your integration

---

## Version History

- **v1.0** (2024): Initial migration from Java to Python
  - Full functional equivalence with Java version
  - Added type hints and comprehensive documentation
  - PEP 8 compliant
  - Enhanced with Python best practices

---

**Last Updated**: 2024
**Python Version**: 3.6+
**Status**: Production Ready ✅
