# Troubleshooting Guide: Java to Python Migration

## Overview

This guide provides solutions to common issues encountered during Java to Python code migration and usage of the converted code.

---

## Table of Contents

1. [Git and Repository Issues](#git-and-repository-issues)
2. [Code Conversion Issues](#code-conversion-issues)
3. [Runtime Issues](#runtime-issues)
4. [Performance Issues](#performance-issues)
5. [Integration Issues](#integration-issues)
6. [Best Practices](#best-practices)

---

## Git and Repository Issues

### Issue 1: Authentication Failure

**Symptom:**
```
Error: Authentication failed
HTTP 401: Unauthorized
```

**Causes:**
- Invalid or expired GitHub Personal Access Token
- Insufficient permissions on the repository
- Token not properly configured

**Solutions:**
1. **Verify Token Validity:**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Check if token is expired
   - Generate new token if needed

2. **Check Token Permissions:**
   - Ensure token has `repo` scope for private repositories
   - For public repos, ensure `public_repo` scope is enabled

3. **Update Token:**
   ```python
   # Use the new token in your configuration
   token = "ghp_YourNewTokenHere"
   ```

### Issue 2: Branch Not Found

**Symptom:**
```
Error: Branch 'main' not found
```

**Solutions:**
1. Verify branch name (some repos use 'master' instead of 'main')
2. Check if branch exists: `git branch -a`
3. Create branch if needed: `git checkout -b main`

### Issue 3: File Upload Failure

**Symptom:**
```
Error: Failed to upload file to GitHub
```

**Solutions:**
1. Check internet connectivity
2. Verify repository write permissions
3. Ensure file size is within GitHub limits (100MB)
4. Check for special characters in file names

---

## Code Conversion Issues

### Issue 4: Unsupported Java Features

**Symptom:**
Certain Java features don't have direct Python equivalents

**Common Cases:**

#### A. Java Reflection API
**Java Code:**
```java
Class<?> clazz = Class.forName("com.example.MyClass");
```

**Python Solution:**
```python
import importlib
module = importlib.import_module("com.example.my_class")
clazz = getattr(module, "MyClass")
```

#### B. Java Annotations
**Java Code:**
```java
@Override
public void method() { }
```

**Python Solution:**
```python
# Use decorators or simply override
def method(self):
    pass
```

#### C. Multiple Inheritance Conflicts
**Java Code:**
```java
class MyClass implements Interface1, Interface2 { }
```

**Python Solution:**
```python
from abc import ABC, abstractmethod

class MyClass(Interface1, Interface2):
    pass  # Python supports multiple inheritance
```

### Issue 5: Type Conversion Errors

**Symptom:**
```
TypeError: unsupported operand type(s)
```

**Solutions:**
1. **Add Type Checking:**
   ```python
   def calculate_discount(amount: float, customer_type: str) -> float:
       if not isinstance(amount, (int, float)):
           raise TypeError("Amount must be numeric")
       if not isinstance(customer_type, str):
           raise TypeError("Customer type must be string")
   ```

2. **Use Type Conversion:**
   ```python
   amount = float(amount)  # Ensure float type
   customer_type = str(customer_type)  # Ensure string type
   ```

### Issue 6: Case Sensitivity Issues

**Symptom:**
String comparisons fail due to case differences

**Solution:**
```python
# Java: "PREMIUM".equalsIgnoreCase(customerType)
# Python: Use .upper() or .lower()
if customer_type.upper() == "PREMIUM":
    # Handle premium customer
```

---

## Runtime Issues

### Issue 7: Import Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'discount_calculator'
```

**Solutions:**
1. **Check Python Path:**
   ```python
   import sys
   print(sys.path)
   ```

2. **Add to Python Path:**
   ```python
   import sys
   sys.path.append('/path/to/output3')
   from discount_calculator import DiscountCalculator
   ```

3. **Use Relative Imports:**
   ```python
   from .discount_calculator import DiscountCalculator
   ```

### Issue 8: Negative Amount Handling

**Symptom:**
Unexpected behavior with negative amounts

**Solution:**
```python
def calculate_discount(amount: float, customer_type: str) -> float:
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    # Rest of the code...
```

### Issue 9: Division by Zero

**Symptom:**
```
ZeroDivisionError: division by zero
```

**Solution:**
```python
if amount == 0:
    return 0.0
# Proceed with calculation
```

---

## Performance Issues

### Issue 10: Slow Execution

**Symptom:**
Code runs slower than expected

**Solutions:**
1. **Use Built-in Functions:**
   ```python
   # Instead of loops, use built-in functions
   total = sum(amounts)  # Faster than manual loop
   ```

2. **Cache Results:**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def calculate_discount(amount: float, customer_type: str) -> float:
       # Cached for repeated calls
   ```

3. **Profile Code:**
   ```python
   import cProfile
   cProfile.run('DiscountCalculator.calculate_discount(5000, "PREMIUM")')
   ```

---

## Integration Issues

### Issue 11: Database Connectivity

**Symptom:**
Java JDBC code needs Python equivalent

**Solution:**
```python
# Use appropriate Python database library
import sqlite3  # or psycopg2, pymysql, etc.

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM customers")
```

### Issue 12: REST API Integration

**Symptom:**
Java HTTP client code needs conversion

**Solution:**
```python
import requests

response = requests.get('https://api.example.com/data')
data = response.json()
```

---

## Best Practices

### 1. Error Handling

```python
def calculate_discount(amount: float, customer_type: str) -> float:
    try:
        # Validation
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        
        # Calculation logic
        discount = 0.0
        # ...
        
        return final_amount
    
    except ValueError as e:
        print(f"Validation error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
```

### 2. Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_discount(amount: float, customer_type: str) -> float:
    logger.info(f"Calculating discount for amount={amount}, type={customer_type}")
    # Calculation logic
    logger.info(f"Final amount: {final_amount}")
    return final_amount
```

### 3. Unit Testing

```python
import unittest

class TestDiscountCalculator(unittest.TestCase):
    def test_premium_discount(self):
        result = DiscountCalculator.calculate_discount(5000, "PREMIUM")
        self.assertEqual(result, 4000.0)
    
    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            DiscountCalculator.calculate_discount(-100, "PREMIUM")

if __name__ == '__main__':
    unittest.main()
```

### 4. Configuration Management

```python
import json

# config.json
{
    "discounts": {
        "PREMIUM": 0.20,
        "STANDARD": 0.10
    },
    "high_value_threshold": 10000,
    "high_value_bonus": 0.05
}

# Load configuration
with open('config.json') as f:
    config = json.load(f)

discount = config['discounts'].get(customer_type.upper(), 0.0)
```

---

## Getting Help

### Resources

1. **Python Documentation:** https://docs.python.org/3/
2. **PEP8 Style Guide:** https://pep8.org/
3. **Type Hints:** https://docs.python.org/3/library/typing.html
4. **GitHub API:** https://docs.github.com/en/rest

### Support Channels

1. **GitHub Issues:** Report bugs or request features
2. **Stack Overflow:** Tag questions with `python` and `java-migration`
3. **Code Review:** Submit pull requests for review

---

## Quick Reference

### Common Java to Python Mappings

| Java | Python |
|------|--------|
| `System.out.println()` | `print()` |
| `String` | `str` |
| `int`, `double` | `int`, `float` |
| `boolean` | `bool` |
| `null` | `None` |
| `true`/`false` | `True`/`False` |
| `&&`, `||` | `and`, `or` |
| `!` | `not` |
| `.equals()` | `==` |
| `.equalsIgnoreCase()` | `.upper() ==` or `.lower() ==` |

---

## Conclusion

This guide covers the most common issues encountered during Java to Python migration. For issues not covered here, please:

1. Check the Python documentation
2. Review the migration report for specific details
3. Consult the README.md for usage instructions
4. Open a GitHub issue for support

---

*Last Updated: 2024*
*Migration Framework Version: 2.0*
