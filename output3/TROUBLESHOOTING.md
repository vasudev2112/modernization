# Troubleshooting Guide - Discount Calculator

This guide provides solutions to common issues you may encounter when using or migrating the Discount Calculator module.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Runtime Errors](#runtime-errors)
3. [Migration Issues](#migration-issues)
4. [Performance Issues](#performance-issues)
5. [Integration Issues](#integration-issues)
6. [Testing Issues](#testing-issues)
7. [Git/GitHub Issues](#gitgithub-issues)

---

## Installation Issues

### Issue 1: Python Version Compatibility

**Symptom:**
```
SyntaxError: invalid syntax
```
or
```
TypeError: unsupported operand type(s)
```

**Cause:** Using Python version older than 3.6

**Solution:**
1. Check your Python version:
   ```bash
   python --version
   ```
2. Upgrade to Python 3.6 or higher:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install python3.8
   
   # On macOS with Homebrew
   brew install python@3.8
   
   # On Windows
   # Download from https://www.python.org/downloads/
   ```

### Issue 2: Module Not Found

**Symptom:**
```python
ModuleNotFoundError: No module named 'discount_calculator'
```

**Cause:** Module not in Python path or wrong directory

**Solution:**

**Option 1:** Run from the same directory
```bash
cd output3
python discount_calculator.py
```

**Option 2:** Add to Python path
```python
import sys
sys.path.append('/path/to/output3')
from discount_calculator import DiscountCalculator
```

**Option 3:** Install as package
```bash
# Create setup.py in output3 folder
pip install -e .
```

---

## Runtime Errors

### Issue 3: Type Error on calculate_discount

**Symptom:**
```python
TypeError: unsupported operand type(s) for *: 'str' and 'float'
```

**Cause:** Passing string instead of number for amount

**Solution:**
```python
# Wrong
DiscountCalculator.calculate_discount("5000", "PREMIUM")

# Correct
DiscountCalculator.calculate_discount(5000, "PREMIUM")
# or
DiscountCalculator.calculate_discount(float("5000"), "PREMIUM")
```

### Issue 4: Unexpected Discount Results

**Symptom:** Discount amount doesn't match expectations

**Cause:** Misunderstanding of discount rules or floating-point precision

**Solution:**

**Check discount rules:**
- Premium: 20% base discount
- Standard: 10% base discount
- High-value (>$10,000): Additional 5% discount
- Unknown type: No discount

**Example calculations:**
```python
# Premium customer, $5,000
# Discount: 20%
# Final: $5,000 - ($5,000 × 0.20) = $4,000
result = DiscountCalculator.calculate_discount(5000, "PREMIUM")
assert result == 4000.0

# Standard customer, $15,000 (high-value)
# Discount: 10% + 5% = 15%
# Final: $15,000 - ($15,000 × 0.15) = $12,750
result = DiscountCalculator.calculate_discount(15000, "STANDARD")
assert result == 12750.0
```

### Issue 5: Floating-Point Precision Issues

**Symptom:**
```python
# Expected: 12750.0
# Got: 12749.999999999998
```

**Cause:** IEEE 754 floating-point arithmetic limitations

**Solution for Financial Applications:**
```python
from decimal import Decimal, ROUND_HALF_UP

def calculate_discount_precise(amount: str, customer_type: str) -> Decimal:
    """Version using Decimal for exact arithmetic"""
    amount_decimal = Decimal(amount)
    discount = Decimal('0.0')
    
    if customer_type.upper() == "PREMIUM":
        discount = Decimal('0.20')
    elif customer_type.upper() == "STANDARD":
        discount = Decimal('0.10')
    
    if amount_decimal > Decimal('10000'):
        discount += Decimal('0.05')
    
    final_amount = amount_decimal - (amount_decimal * discount)
    return final_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

# Usage
result = calculate_discount_precise('15000', 'STANDARD')
print(result)  # Exactly: 12750.00
```

---

## Migration Issues

### Issue 6: Java to Python Conversion Discrepancies

**Symptom:** Python output differs from Java output

**Cause:** Different handling of edge cases or data types

**Solution:**

**Check these common differences:**

1. **String comparison:**
   ```java
   // Java
   "PREMIUM".equalsIgnoreCase(customerType)
   ```
   ```python
   # Python
   customer_type.upper() == "PREMIUM"
   ```

2. **Integer division:**
   ```java
   // Java: 5 / 2 = 2 (integer division)
   int result = 5 / 2;
   ```
   ```python
   # Python 3: 5 / 2 = 2.5 (float division)
   result = 5 / 2
   # For integer division in Python:
   result = 5 // 2  # = 2
   ```

3. **Null vs None:**
   ```java
   // Java
   if (value == null)
   ```
   ```python
   # Python
   if value is None:
   ```

### Issue 7: Missing Java Features

**Symptom:** Java code uses features not available in Python

**Common Java features and Python alternatives:**

| Java Feature | Python Alternative |
|--------------|--------------------|
| `synchronized` | `threading.Lock()` |
| `interface` | Abstract Base Class (ABC) |
| `enum` | `enum.Enum` |
| `try-with-resources` | `with` statement |
| `Optional<T>` | `Optional` from typing or None |
| Annotations | Decorators |
| Generics | Type hints with typing module |

**Example:**
```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

class CustomerType(Enum):
    PREMIUM = "PREMIUM"
    STANDARD = "STANDARD"

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float:
        pass
```

---

## Performance Issues

### Issue 8: Slow Performance with Large Datasets

**Symptom:** Processing many discount calculations is slow

**Solution:**

**Option 1: Batch Processing**
```python
def calculate_discounts_batch(amounts: list, customer_types: list) -> list:
    """Process multiple discounts efficiently"""
    return [
        DiscountCalculator.calculate_discount(amount, customer_type)
        for amount, customer_type in zip(amounts, customer_types)
    ]

# Usage
amounts = [5000, 15000, 2000]
types = ["PREMIUM", "STANDARD", "UNKNOWN"]
results = calculate_discounts_batch(amounts, types)
```

**Option 2: NumPy for Large-Scale Calculations**
```python
import numpy as np

def calculate_discounts_numpy(amounts: np.ndarray, is_premium: np.ndarray) -> np.ndarray:
    """Vectorized discount calculation"""
    discounts = np.where(is_premium, 0.20, 0.10)
    high_value = amounts > 10000
    discounts = np.where(high_value, discounts + 0.05, discounts)
    return amounts * (1 - discounts)

# Usage
amounts = np.array([5000, 15000, 2000])
is_premium = np.array([True, False, False])
results = calculate_discounts_numpy(amounts, is_premium)
```

---

## Integration Issues

### Issue 9: Integration with Web Frameworks

**Symptom:** Issues using the module in Flask/Django/FastAPI

**Solution for Flask:**
```python
from flask import Flask, request, jsonify
from discount_calculator import DiscountCalculator

app = Flask(__name__)

@app.route('/calculate-discount', methods=['POST'])
def calculate_discount():
    try:
        data = request.get_json()
        amount = float(data['amount'])
        customer_type = data['customer_type']
        
        result = DiscountCalculator.calculate_discount(amount, customer_type)
        
        return jsonify({
            'original_amount': amount,
            'customer_type': customer_type,
            'final_amount': result,
            'discount_applied': amount - result
        })
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

**Solution for FastAPI:**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from discount_calculator import DiscountCalculator

app = FastAPI()

class DiscountRequest(BaseModel):
    amount: float
    customer_type: str

class DiscountResponse(BaseModel):
    original_amount: float
    customer_type: str
    final_amount: float
    discount_applied: float

@app.post("/calculate-discount", response_model=DiscountResponse)
def calculate_discount(request: DiscountRequest):
    if request.amount < 0:
        raise HTTPException(status_code=400, detail="Amount cannot be negative")
    
    final_amount = DiscountCalculator.calculate_discount(
        request.amount, 
        request.customer_type
    )
    
    return DiscountResponse(
        original_amount=request.amount,
        customer_type=request.customer_type,
        final_amount=final_amount,
        discount_applied=request.amount - final_amount
    )
```

### Issue 10: Database Integration

**Symptom:** Need to store discount calculations in database

**Solution with SQLAlchemy:**
```python
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from discount_calculator import DiscountCalculator

Base = declarative_base()

class DiscountTransaction(Base):
    __tablename__ = 'discount_transactions'
    
    id = Column(Integer, primary_key=True)
    original_amount = Column(Float, nullable=False)
    customer_type = Column(String(50), nullable=False)
    final_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

def save_discount_calculation(amount: float, customer_type: str, session):
    final_amount = DiscountCalculator.calculate_discount(amount, customer_type)
    
    transaction = DiscountTransaction(
        original_amount=amount,
        customer_type=customer_type,
        final_amount=final_amount,
        discount_amount=amount - final_amount
    )
    
    session.add(transaction)
    session.commit()
    return transaction
```

---

## Testing Issues

### Issue 11: Test Failures

**Symptom:** Unit tests fail unexpectedly

**Solution:**

**Check floating-point comparisons:**
```python
import pytest

# Wrong - may fail due to floating-point precision
def test_discount_wrong():
    result = DiscountCalculator.calculate_discount(15000, "STANDARD")
    assert result == 12750.0

# Correct - use approximate comparison
def test_discount_correct():
    result = DiscountCalculator.calculate_discount(15000, "STANDARD")
    assert pytest.approx(result, rel=1e-9) == 12750.0
    # or
    assert abs(result - 12750.0) < 0.01
```

### Issue 12: Missing Test Coverage

**Symptom:** Need to improve test coverage

**Solution - Comprehensive Test Suite:**
```python
import pytest
from discount_calculator import DiscountCalculator

class TestDiscountCalculator:
    
    @pytest.mark.parametrize("amount,customer_type,expected", [
        (5000, "PREMIUM", 4000.0),
        (5000, "premium", 4000.0),
        (5000, "STANDARD", 4500.0),
        (15000, "PREMIUM", 11250.0),
        (15000, "STANDARD", 12750.0),
        (2000, "UNKNOWN", 2000.0),
        (0, "PREMIUM", 0.0),
        (10000, "STANDARD", 9000.0),
        (10001, "STANDARD", 8500.85),
    ])
    def test_various_scenarios(self, amount, customer_type, expected):
        result = DiscountCalculator.calculate_discount(amount, customer_type)
        assert pytest.approx(result, rel=1e-9) == expected
    
    def test_negative_amount(self):
        result = DiscountCalculator.calculate_discount(-100, "PREMIUM")
        assert result == 0.0
    
    def test_edge_cases(self):
        # Very large amount
        result = DiscountCalculator.calculate_discount(1000000, "PREMIUM")
        assert result == 750000.0
        
        # Exactly at threshold
        result = DiscountCalculator.calculate_discount(10000, "PREMIUM")
        assert result == 8000.0
```

---

## Git/GitHub Issues

### Issue 13: GitHub Authentication Failure

**Symptom:**
```
HTTP 401: Unauthorized
```

**Solution:**

1. **Verify token is valid:**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Check token hasn't expired
   - Ensure token has required permissions (repo access)

2. **Regenerate token if needed:**
   - Create new token with `repo` scope
   - Update your configuration

3. **Check token format:**
   ```python
   # Correct format
   token = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```

### Issue 14: Push Rejected

**Symptom:**
```
Error: Updates were rejected because the remote contains work that you do not have locally
```

**Solution:**
```bash
# Pull latest changes first
git pull origin main

# Resolve any conflicts
# Then push again
git push origin main
```

---

## Additional Resources

### Documentation
- [README.md](README.md) - Quick start guide
- [MIGRATION_REPORT.md](MIGRATION_REPORT.md) - Detailed migration documentation
- Python Documentation: https://docs.python.org/3/
- PEP 8 Style Guide: https://pep8.org/

### Support Channels
1. Check inline code documentation
2. Review migration report for known issues
3. Consult Python best practices documentation
4. Review test cases for usage examples

### Common Commands

```bash
# Run the module
python discount_calculator.py

# Run tests
pytest test_discount_calculator.py -v

# Check code style
flake8 discount_calculator.py

# Type checking
mypy discount_calculator.py

# Format code
black discount_calculator.py
```

---

## Quick Reference

### Error Code Reference

| Error | Cause | Solution |
|-------|-------|----------|
| ModuleNotFoundError | Module not in path | Add to path or run from correct directory |
| TypeError | Wrong data type | Check parameter types |
| AttributeError | Method doesn't exist | Check spelling and class name |
| ValueError | Invalid value | Validate input before calling |
| SyntaxError | Python version too old | Upgrade to Python 3.6+ |

### Contact

For issues not covered in this guide:
1. Review the migration report
2. Check the README documentation
3. Consult Python documentation
4. Review code comments and docstrings

---

**Last Updated:** 2024
**Document Version:** 1.0
