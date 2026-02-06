# Java to Python Migration - Troubleshooting Guide

## Table of Contents
1. [Common Migration Issues](#common-migration-issues)
2. [Git Integration Issues](#git-integration-issues)
3. [Code Conversion Issues](#code-conversion-issues)
4. [Runtime Issues](#runtime-issues)
5. [Best Practices](#best-practices)
6. [FAQ](#faq)

---

## Common Migration Issues

### Issue 1: Authentication Failure

**Symptom:**
```
Error: Authentication failed
HTTP 401: Unauthorized
```

**Causes:**
- Invalid or expired GitHub token
- Insufficient permissions on the repository
- Token not properly formatted

**Solutions:**
1. **Verify Token Validity:**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Check if token is still active
   - Ensure token has required scopes: `repo`, `write:packages`

2. **Generate New Token:**
   - Navigate to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (full control)
   - Copy and use the new token

3. **Check Repository Access:**
   - Verify you have write access to the repository
   - Check if repository is private and token has appropriate permissions

---

### Issue 2: File Not Found

**Symptom:**
```
Error: File not found in repository
404: Not Found
```

**Causes:**
- Incorrect file path
- File doesn't exist in specified branch
- Folder name mismatch

**Solutions:**
1. **Verify File Path:**
   ```
   Correct: folder_name="input", file_name="java_test.txt"
   Incorrect: folder_name="input/", file_name="/java_test.txt"
   ```

2. **Check Branch Name:**
   - Ensure branch name is correct (case-sensitive)
   - Common branch names: `main`, `master`, `develop`

3. **Verify Repository Structure:**
   - Navigate to repository on GitHub
   - Confirm folder and file exist at specified location

---

### Issue 3: Conversion Errors

**Symptom:**
```
Error: Unable to convert Java construct to Python
Unsupported feature: [feature_name]
```

**Causes:**
- Complex Java features without direct Python equivalent
- Reflection API usage
- Java-specific annotations
- Multi-threading with synchronized blocks

**Solutions:**

1. **Reflection API:**
   - **Java:**
     ```java
     Class<?> clazz = Class.forName("com.example.MyClass");
     ```
   - **Python Alternative:**
     ```python
     import importlib
     module = importlib.import_module("com.example.my_class")
     ```

2. **Synchronized Blocks:**
   - **Java:**
     ```java
     synchronized(object) { /* code */ }
     ```
   - **Python Alternative:**
     ```python
     from threading import Lock
     lock = Lock()
     with lock:
         # code
     ```

3. **Annotations:**
   - **Java:**
     ```java
     @Override
     public void method() { }
     ```
   - **Python Alternative:**
     ```python
     # Use decorators or type hints
     from typing import override  # Python 3.12+
     @override
     def method(self) -> None:
         pass
     ```

---

## Git Integration Issues

### Issue 4: Push Rejected

**Symptom:**
```
Error: Push rejected
Remote contains work that you do not have locally
```

**Causes:**
- Remote branch has commits not in local
- Merge conflict
- Protected branch rules

**Solutions:**
1. **Pull Latest Changes:**
   ```bash
   git pull origin main --rebase
   ```

2. **Check Branch Protection:**
   - Go to repository Settings → Branches
   - Review branch protection rules
   - Ensure you have permission to push

3. **Create Pull Request Instead:**
   - Push to a feature branch
   - Create PR to merge into main

---

### Issue 5: Large File Upload

**Symptom:**
```
Error: File size exceeds GitHub limit
File size: 100MB, Limit: 100MB
```

**Solutions:**
1. **Use Git LFS:**
   ```bash
   git lfs install
   git lfs track "*.jar"
   git add .gitattributes
   ```

2. **Split Large Files:**
   - Break down large files into smaller modules
   - Use compression if applicable

3. **Use External Storage:**
   - Store large files in cloud storage
   - Reference them in code

---

## Code Conversion Issues

### Issue 6: Type Mismatch

**Java to Python Type Mapping:**

| Java Type | Python Type | Notes |
|-----------|-------------|-------|
| `int` | `int` | Direct mapping |
| `long` | `int` | Python 3 int is arbitrary precision |
| `float` | `float` | Direct mapping |
| `double` | `float` | Python float is double precision |
| `boolean` | `bool` | Direct mapping |
| `String` | `str` | Direct mapping |
| `char` | `str` | Single character string |
| `List<T>` | `List[T]` | Use typing module |
| `Map<K,V>` | `Dict[K,V]` | Use typing module |
| `Set<T>` | `Set[T]` | Use typing module |
| `null` | `None` | Direct mapping |

---

### Issue 7: Method Naming Conflicts

**Java vs Python Naming Conventions:**

| Java | Python | Example |
|------|--------|----------|
| camelCase | snake_case | `calculateTotal` → `calculate_total` |
| PascalCase | PascalCase | `MyClass` → `MyClass` |
| UPPER_CASE | UPPER_CASE | `MAX_VALUE` → `MAX_VALUE` |

**Solution:**
```python
# Use automated conversion
def to_snake_case(name: str) -> str:
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
```

---

## Runtime Issues

### Issue 8: Import Errors

**Symptom:**
```python
ModuleNotFoundError: No module named 'xyz'
```

**Solutions:**
1. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create requirements.txt:**
   ```txt
   # Add Python equivalents of Java dependencies
   requests==2.31.0  # For HTTP (like Apache HttpClient)
   pytest==7.4.0     # For testing (like JUnit)
   ```

3. **Check Python Path:**
   ```python
   import sys
   print(sys.path)
   ```

---

### Issue 9: Performance Issues

**Symptom:**
Python code runs slower than Java equivalent

**Solutions:**
1. **Use Built-in Functions:**
   ```python
   # Slow
   result = []
   for item in items:
       result.append(item * 2)
   
   # Fast
   result = [item * 2 for item in items]
   ```

2. **Use NumPy for Numerical Operations:**
   ```python
   import numpy as np
   array = np.array([1, 2, 3, 4, 5])
   result = array * 2  # Vectorized operation
   ```

3. **Profile Your Code:**
   ```python
   import cProfile
   cProfile.run('your_function()')
   ```

---

## Best Practices

### 1. Code Organization

```
project/
├── src/
│   ├── __init__.py
│   ├── module1.py
│   └── module2.py
├── tests/
│   ├── __init__.py
│   ├── test_module1.py
│   └── test_module2.py
├── requirements.txt
├── README.md
└── setup.py
```

### 2. Documentation

```python
def calculate_discount(amount: float, customer_type: str) -> float:
    """
    Calculate discount based on customer type and amount.
    
    Args:
        amount: Purchase amount in dollars
        customer_type: Type of customer (PREMIUM/STANDARD)
    
    Returns:
        Final amount after applying discount
    
    Raises:
        ValueError: If amount is negative
    
    Examples:
        >>> calculate_discount(1000, "PREMIUM")
        800.0
    """
    pass
```

### 3. Testing

```python
import pytest

def test_premium_discount():
    result = calculate_discount(5000, "PREMIUM")
    assert result == 4000.0

def test_invalid_amount():
    with pytest.raises(ValueError):
        calculate_discount(-100, "PREMIUM")
```

### 4. Error Handling

```python
def safe_calculate(amount: float, customer_type: str) -> float:
    try:
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        return calculate_discount(amount, customer_type)
    except ValueError as e:
        print(f"Error: {e}")
        return 0.0
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
```

---

## FAQ

### Q1: How do I handle Java interfaces in Python?

**A:** Use Abstract Base Classes (ABC)

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        # Implementation
        return True
```

### Q2: How do I handle Java generics in Python?

**A:** Use type hints from typing module

```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, items: List[T]):
        self.items = items
    
    def get_first(self) -> T:
        return self.items[0]
```

### Q3: How do I handle Java exceptions in Python?

**A:** Create custom exception classes

```python
class InvalidCustomerTypeError(Exception):
    """Raised when customer type is invalid"""
    pass

def validate_customer(customer_type: str) -> None:
    if customer_type not in ["PREMIUM", "STANDARD"]:
        raise InvalidCustomerTypeError(f"Invalid type: {customer_type}")
```

### Q4: How do I migrate Java streams to Python?

**A:** Use list comprehensions, map, filter, and itertools

```python
# Java: list.stream().filter(x -> x > 5).map(x -> x * 2).collect()
# Python:
result = [x * 2 for x in items if x > 5]

# Or using map and filter:
result = list(map(lambda x: x * 2, filter(lambda x: x > 5, items)))
```

### Q5: How do I handle Java properties files in Python?

**A:** Use configparser or python-dotenv

```python
import configparser

config = configparser.ConfigParser()
config.read('config.properties')
value = config['section']['key']

# Or use .env files:
from dotenv import load_dotenv
import os

load_dotenv()
value = os.getenv('KEY')
```

---

## Getting Help

### Resources
- **Python Documentation:** https://docs.python.org/3/
- **PEP 8 Style Guide:** https://pep8.org/
- **Type Hints Guide:** https://docs.python.org/3/library/typing.html
- **GitHub API Documentation:** https://docs.github.com/en/rest

### Support Channels
1. Check this troubleshooting guide
2. Review MIGRATION_REPORT.md for specific issues
3. Consult Python and GitHub documentation
4. Review converted code for inline comments

---

**Last Updated:** 2024
**Version:** 1.0
**Maintained By:** Senior Code Migration and Git Integration Automation Agent
