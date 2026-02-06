# Troubleshooting Guide - Java to Python Migration

## Table of Contents
1. [Common Migration Issues](#common-migration-issues)
2. [Runtime Errors](#runtime-errors)
3. [Environment Issues](#environment-issues)
4. [Git Integration Issues](#git-integration-issues)
5. [Code Execution Issues](#code-execution-issues)
6. [Performance Issues](#performance-issues)
7. [Quick Reference](#quick-reference)

---

## Common Migration Issues

### Issue 1: Python Version Compatibility

**Symptom:**
```
SyntaxError: invalid syntax
  def calculate_discount(amount: float, customer_type: str) -> float:
                              ^
```

**Cause:** Using Python version older than 3.6 which doesn't support type hints.

**Solution:**
```bash
# Check your Python version
python --version

# If version is < 3.6, upgrade Python
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.8

# On macOS with Homebrew
brew install python@3.8

# On Windows
# Download from https://www.python.org/downloads/
```

**Alternative Solution:** Remove type hints if upgrade is not possible:
```python
# Instead of:
def calculate_discount(amount: float, customer_type: str) -> float:

# Use:
def calculate_discount(amount, customer_type):
```

---

### Issue 2: Module Import Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'discount_calculator'
```

**Cause:** Python cannot find the module in the current path.

**Solution 1:** Run from the correct directory
```bash
cd /path/to/output4
python discount_calculator.py
```

**Solution 2:** Add directory to PYTHONPATH
```bash
# Linux/macOS
export PYTHONPATH="${PYTHONPATH}:/path/to/output4"

# Windows
set PYTHONPATH=%PYTHONPATH%;C:\path\to\output4
```

**Solution 3:** Use absolute imports
```python
import sys
sys.path.append('/path/to/output4')
from discount_calculator import DiscountCalculator
```

---

### Issue 3: Encoding Issues

**Symptom:**
```
UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d
```

**Cause:** File encoding mismatch between systems.

**Solution:**
```python
# Always specify UTF-8 encoding when reading files
with open('discount_calculator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# For writing files
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(content)
```

---

## Runtime Errors

### Issue 4: Type Errors

**Symptom:**
```
TypeError: unsupported operand type(s) for -: 'str' and 'float'
```

**Cause:** Passing string instead of numeric value for amount.

**Solution:**
```python
# Wrong:
result = DiscountCalculator.calculate_discount("5000", "PREMIUM")

# Correct:
result = DiscountCalculator.calculate_discount(5000, "PREMIUM")

# Or convert string to float:
amount_str = "5000"
result = DiscountCalculator.calculate_discount(float(amount_str), "PREMIUM")
```

**Prevention:** Add input validation
```python
@staticmethod
def calculate_discount(amount, customer_type):
    # Validate inputs
    if not isinstance(amount, (int, float)):
        raise TypeError(f"Amount must be numeric, got {type(amount)}")
    if not isinstance(customer_type, str):
        raise TypeError(f"Customer type must be string, got {type(customer_type)}")
    
    # Rest of the code...
```

---

### Issue 5: Attribute Errors

**Symptom:**
```
AttributeError: 'str' object has no attribute 'upper'
```

**Cause:** Passing None or non-string value for customer_type.

**Solution:**
```python
# Add None check
if customer_type is None:
    customer_type = "STANDARD"  # Default value

# Or handle in the method
if customer_type and customer_type.upper() == "PREMIUM":
    discount = 0.20
```

---

## Environment Issues

### Issue 6: Missing Dependencies

**Symptom:**
```
ImportError: No module named 'typing'
```

**Cause:** Very old Python version (< 3.5).

**Solution:**
```bash
# Upgrade Python to 3.6+
python --version

# If cannot upgrade, install typing backport
pip install typing
```

---

### Issue 7: Permission Errors

**Symptom:**
```
PermissionError: [Errno 13] Permission denied: 'discount_calculator.py'
```

**Cause:** Insufficient file permissions.

**Solution:**
```bash
# Linux/macOS - Add execute permission
chmod +x discount_calculator.py

# Or run with python explicitly
python discount_calculator.py

# Windows - Run as administrator or check file properties
```

---

## Git Integration Issues

### Issue 8: Authentication Failure

**Symptom:**
```
Error: Authentication failed
```

**Cause:** Invalid or expired GitHub token.

**Solution:**
```bash
# 1. Generate new GitHub Personal Access Token
# Go to: GitHub Settings → Developer settings → Personal access tokens
# Create token with 'repo' scope

# 2. Update token in your configuration
# Verify token has correct permissions:
# - repo (full control)
# - workflow (if using GitHub Actions)

# 3. Test token
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
```

---

### Issue 9: Push Rejected

**Symptom:**
```
Error: Updates were rejected because the remote contains work that you do not have locally
```

**Cause:** Remote branch has changes not in local copy.

**Solution:**
```bash
# Pull latest changes first
git pull origin main

# Resolve any conflicts
# Then push again
git push origin main

# Or force push (use with caution)
git push -f origin main
```

---

### Issue 10: Branch Not Found

**Symptom:**
```
Error: Branch 'main' not found
```

**Cause:** Branch name might be 'master' instead of 'main'.

**Solution:**
```bash
# List all branches
git branch -a

# Use the correct branch name
git checkout master  # or main

# Or create the branch
git checkout -b main
```

---

## Code Execution Issues

### Issue 11: Incorrect Output Values

**Symptom:** Calculated discount doesn't match expected value.

**Cause:** Logic error or floating-point precision issues.

**Solution:**
```python
# Use decimal for precise calculations
from decimal import Decimal

def calculate_discount(amount, customer_type):
    amount = Decimal(str(amount))
    discount = Decimal('0.0')
    
    if customer_type.upper() == "PREMIUM":
        discount = Decimal('0.20')
    elif customer_type.upper() == "STANDARD":
        discount = Decimal('0.10')
    
    if amount > Decimal('10000'):
        discount += Decimal('0.05')
    
    final_amount = amount - (amount * discount)
    return float(final_amount)
```

**Debugging:**
```python
# Add debug prints
def calculate_discount(amount, customer_type):
    print(f"DEBUG: Input amount={amount}, customer_type={customer_type}")
    
    discount = 0.0
    if customer_type.upper() == "PREMIUM":
        discount = 0.20
        print(f"DEBUG: Applied PREMIUM discount: {discount}")
    
    if amount > 10000:
        discount += 0.05
        print(f"DEBUG: Applied high-value discount, total: {discount}")
    
    final_amount = amount - (amount * discount)
    print(f"DEBUG: Final amount: {final_amount}")
    return final_amount
```

---

### Issue 12: Case Sensitivity Issues

**Symptom:** Discount not applied for "premium" (lowercase).

**Cause:** String comparison is case-sensitive.

**Solution:** Already handled in the code with `.upper()`
```python
# This handles all cases: "premium", "PREMIUM", "Premium"
if customer_type.upper() == "PREMIUM":
    discount = 0.20
```

---

## Performance Issues

### Issue 13: Slow Execution

**Symptom:** Code runs slower than expected.

**Cause:** Multiple reasons possible.

**Solution:**
```python
# Profile the code
import cProfile
import pstats

def profile_code():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run your code
    for i in range(10000):
        DiscountCalculator.calculate_discount(5000, "PREMIUM")
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)

profile_code()
```

---

### Issue 14: Memory Issues

**Symptom:** High memory usage.

**Cause:** Creating too many objects or not releasing resources.

**Solution:**
```python
# Monitor memory usage
import tracemalloc

tracemalloc.start()

# Your code here
for i in range(10000):
    result = DiscountCalculator.calculate_discount(5000, "PREMIUM")

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 10**6}MB")
print(f"Peak memory usage: {peak / 10**6}MB")
tracemalloc.stop()
```

---

## Quick Reference

### Command Cheat Sheet

```bash
# Check Python version
python --version

# Run the script
python discount_calculator.py

# Run with debugging
python -m pdb discount_calculator.py

# Check syntax without running
python -m py_compile discount_calculator.py

# Format code with black
pip install black
black discount_calculator.py

# Lint code with pylint
pip install pylint
pylint discount_calculator.py

# Run type checking
pip install mypy
mypy discount_calculator.py
```

### Common Error Codes

| Error Code | Meaning | Quick Fix |
|------------|---------|----------|
| SyntaxError | Invalid Python syntax | Check Python version, review code |
| TypeError | Wrong data type | Validate input types |
| AttributeError | Missing attribute/method | Check object type, verify spelling |
| ImportError | Cannot import module | Check PYTHONPATH, install dependencies |
| NameError | Variable not defined | Check variable names, scope |
| ValueError | Invalid value | Validate input ranges |

### Testing Commands

```bash
# Run basic tests
python -c "from discount_calculator import DiscountCalculator; print(DiscountCalculator.calculate_discount(5000, 'PREMIUM'))"

# Expected output: 4000.0

# Run all test cases
python -c "
from discount_calculator import DiscountCalculator
assert DiscountCalculator.calculate_discount(5000, 'PREMIUM') == 4000.0
assert DiscountCalculator.calculate_discount(15000, 'STANDARD') == 12750.0
assert DiscountCalculator.calculate_discount(2000, 'UNKNOWN') == 2000.0
print('All tests passed!')
"
```

---

## Getting Help

### Debug Checklist

- [ ] Python version is 3.6 or higher
- [ ] All files are in the correct directory
- [ ] File permissions are correct
- [ ] No syntax errors (run py_compile)
- [ ] Input types are correct
- [ ] PYTHONPATH is set correctly (if needed)
- [ ] GitHub token is valid (if using Git)
- [ ] Network connection is working (if using Git)

### Logging for Debugging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='discount_calculator.log'
)

logger = logging.getLogger(__name__)

# Add to your code
def calculate_discount(amount, customer_type):
    logger.debug(f"Starting calculation: amount={amount}, type={customer_type}")
    # ... rest of code
    logger.info(f"Calculation complete: final_amount={final_amount}")
    return final_amount
```

---

## Additional Resources

- **Python Documentation:** https://docs.python.org/3/
- **PEP 8 Style Guide:** https://www.python.org/dev/peps/pep-0008/
- **GitHub API Documentation:** https://docs.github.com/en/rest
- **Python Debugging:** https://docs.python.org/3/library/pdb.html

---

**Last Updated:** 2024
**Version:** 1.0
**Status:** Active
