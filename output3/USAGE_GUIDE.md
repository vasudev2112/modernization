# Discount Calculator - Usage Guide

## Overview

The Discount Calculator is a Python module that calculates final purchase amounts after applying customer-type-based discounts and high-value purchase bonuses. This guide provides comprehensive instructions for using the converted Python code.

---

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [API Reference](#api-reference)
4. [Usage Examples](#usage-examples)
5. [Best Practices](#best-practices)
6. [Error Handling](#error-handling)
7. [Advanced Usage](#advanced-usage)
8. [FAQ](#faq)

---

## Installation

### Prerequisites

- Python 3.6 or higher
- No external dependencies required (uses Python standard library only)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vasudev2112/modernization.git
   cd modernization/output3
   ```

2. **Verify Python version**:
   ```bash
   python --version
   # Should show Python 3.6 or higher
   ```

3. **Test the installation**:
   ```bash
   python discount_calculator.py
   ```

---

## Quick Start

### Running as a Script

```bash
python discount_calculator.py
```

**Expected Output**:
```
Premium customer with $5000 purchase: $4000.0
Standard customer with $15000 purchase: $12750.0
Unknown customer type with $2000 purchase: $2000.0
```

### Using as a Module

```python
from discount_calculator import DiscountCalculator

# Calculate discount
final_amount = DiscountCalculator.calculate_discount(5000, "PREMIUM")
print(f"Final amount: ${final_amount}")
```

---

## API Reference

### Class: DiscountCalculator

A static utility class for calculating discounts based on customer type and purchase amount.

#### Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `PREMIUM` | "PREMIUM" | Premium customer type identifier |
| `STANDARD` | "STANDARD" | Standard customer type identifier |
| `PREMIUM_DISCOUNT` | 0.20 | 20% discount for premium customers |
| `STANDARD_DISCOUNT` | 0.10 | 10% discount for standard customers |
| `HIGH_VALUE_ADDITIONAL_DISCOUNT` | 0.05 | Additional 5% for high-value purchases |
| `HIGH_VALUE_THRESHOLD` | 10000 | Threshold for high-value purchase bonus |

#### Method: calculate_discount()

```python
@staticmethod
def calculate_discount(amount: float, customer_type: str) -> float
```

**Description**: Calculates the final amount after applying applicable discounts.

**Parameters**:
- `amount` (float): Original purchase amount (must be non-negative)
- `customer_type` (str): Customer type - "PREMIUM", "STANDARD", or any other value

**Returns**:
- `float`: Final amount after discount (minimum 0.0)

**Discount Rules**:
1. **Premium Customers**: 20% discount
2. **Standard Customers**: 10% discount
3. **Other Customer Types**: 0% discount
4. **High-Value Bonus**: Additional 5% discount for purchases over $10,000
5. **Negative Protection**: Final amount cannot be negative

**Examples**:
```python
# Premium customer, regular purchase
DiscountCalculator.calculate_discount(5000, "PREMIUM")
# Returns: 4000.0 (20% discount)

# Standard customer, high-value purchase
DiscountCalculator.calculate_discount(15000, "STANDARD")
# Returns: 12750.0 (10% + 5% = 15% discount)

# Unknown customer type
DiscountCalculator.calculate_discount(2000, "UNKNOWN")
# Returns: 2000.0 (0% discount)

# Premium customer, high-value purchase
DiscountCalculator.calculate_discount(12000, "PREMIUM")
# Returns: 9000.0 (20% + 5% = 25% discount)
```

---

## Usage Examples

### Example 1: Basic Usage

```python
from discount_calculator import DiscountCalculator

# Calculate discount for a premium customer
amount = 5000
customer_type = "PREMIUM"

final_amount = DiscountCalculator.calculate_discount(amount, customer_type)
print(f"Original: ${amount}")
print(f"Customer Type: {customer_type}")
print(f"Final Amount: ${final_amount}")
print(f"You saved: ${amount - final_amount}")
```

**Output**:
```
Original: $5000
Customer Type: PREMIUM
Final Amount: $4000.0
You saved: $1000.0
```

### Example 2: Processing Multiple Orders

```python
from discount_calculator import DiscountCalculator

orders = [
    {"amount": 5000, "customer_type": "PREMIUM"},
    {"amount": 15000, "customer_type": "STANDARD"},
    {"amount": 2000, "customer_type": "GUEST"},
    {"amount": 12000, "customer_type": "PREMIUM"},
]

total_original = 0
total_final = 0

for order in orders:
    amount = order["amount"]
    customer_type = order["customer_type"]
    final = DiscountCalculator.calculate_discount(amount, customer_type)
    
    total_original += amount
    total_final += final
    
    print(f"{customer_type}: ${amount} → ${final}")

print(f"\nTotal Original: ${total_original}")
print(f"Total After Discounts: ${total_final}")
print(f"Total Savings: ${total_original - total_final}")
```

### Example 3: Interactive Calculator

```python
from discount_calculator import DiscountCalculator

def interactive_calculator():
    print("=== Discount Calculator ===")
    print("Customer Types: PREMIUM, STANDARD, or OTHER")
    print("High-value bonus applies to purchases over $10,000\n")
    
    while True:
        try:
            amount = float(input("Enter purchase amount (or 0 to exit): $"))
            if amount == 0:
                break
            
            customer_type = input("Enter customer type: ").strip()
            
            final = DiscountCalculator.calculate_discount(amount, customer_type)
            discount_amount = amount - final
            discount_percent = (discount_amount / amount * 100) if amount > 0 else 0
            
            print(f"\nOriginal Amount: ${amount:.2f}")
            print(f"Discount Applied: {discount_percent:.1f}%")
            print(f"Discount Amount: ${discount_amount:.2f}")
            print(f"Final Amount: ${final:.2f}\n")
            
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    interactive_calculator()
```

### Example 4: Integration with E-commerce System

```python
from discount_calculator import DiscountCalculator

class ShoppingCart:
    def __init__(self, customer_type):
        self.customer_type = customer_type
        self.items = []
    
    def add_item(self, name, price, quantity=1):
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })
    
    def calculate_total(self):
        subtotal = sum(item["price"] * item["quantity"] for item in self.items)
        final_total = DiscountCalculator.calculate_discount(
            subtotal, 
            self.customer_type
        )
        discount = subtotal - final_total
        
        return {
            "subtotal": subtotal,
            "discount": discount,
            "final_total": final_total
        }
    
    def print_receipt(self):
        print("=== RECEIPT ===")
        print(f"Customer Type: {self.customer_type}\n")
        
        for item in self.items:
            total = item["price"] * item["quantity"]
            print(f"{item['name']}: ${item['price']} x {item['quantity']} = ${total}")
        
        totals = self.calculate_total()
        print(f"\nSubtotal: ${totals['subtotal']:.2f}")
        print(f"Discount: -${totals['discount']:.2f}")
        print(f"Final Total: ${totals['final_total']:.2f}")

# Usage
cart = ShoppingCart("PREMIUM")
cart.add_item("Laptop", 1200, 1)
cart.add_item("Mouse", 50, 2)
cart.add_item("Keyboard", 100, 1)
cart.print_receipt()
```

---

## Best Practices

### 1. Input Validation

Always validate inputs before passing to the calculator:

```python
def safe_calculate_discount(amount, customer_type):
    # Validate amount
    if not isinstance(amount, (int, float)):
        raise TypeError("Amount must be a number")
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    
    # Validate customer type
    if not isinstance(customer_type, str):
        raise TypeError("Customer type must be a string")
    
    return DiscountCalculator.calculate_discount(amount, customer_type)
```

### 2. Use Constants

Reference the class constants instead of hardcoding values:

```python
# Good
if customer_type == DiscountCalculator.PREMIUM:
    print("Premium customer detected")

# Avoid
if customer_type == "PREMIUM":
    print("Premium customer detected")
```

### 3. Error Handling

Implement proper error handling:

```python
try:
    final = DiscountCalculator.calculate_discount(amount, customer_type)
except Exception as e:
    print(f"Error calculating discount: {e}")
    final = amount  # Fallback to original amount
```

### 4. Logging

Add logging for audit trails:

```python
import logging
from discount_calculator import DiscountCalculator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_with_logging(amount, customer_type):
    logger.info(f"Calculating discount: amount=${amount}, type={customer_type}")
    final = DiscountCalculator.calculate_discount(amount, customer_type)
    discount = amount - final
    logger.info(f"Discount applied: ${discount} ({discount/amount*100:.1f}%)")
    return final
```

---

## Error Handling

### Common Issues and Solutions

#### Issue: Type Errors

```python
# Problem: Passing wrong types
DiscountCalculator.calculate_discount("5000", "PREMIUM")  # String instead of number

# Solution: Convert to appropriate type
amount = float("5000")
DiscountCalculator.calculate_discount(amount, "PREMIUM")
```

#### Issue: Case Sensitivity

```python
# The method handles case-insensitive customer types
DiscountCalculator.calculate_discount(5000, "premium")  # Works
DiscountCalculator.calculate_discount(5000, "PREMIUM")  # Works
DiscountCalculator.calculate_discount(5000, "Premium")  # Works
```

---

## Advanced Usage

### Custom Discount Rules

Extend the calculator with custom rules:

```python
from discount_calculator import DiscountCalculator

class ExtendedDiscountCalculator(DiscountCalculator):
    VIP_DISCOUNT = 0.30
    
    @staticmethod
    def calculate_discount(amount, customer_type, promo_code=None):
        # Apply base discount
        final = DiscountCalculator.calculate_discount(amount, customer_type)
        
        # Apply promo code discount
        if promo_code == "SAVE10":
            final *= 0.90
        elif promo_code == "VIP":
            final *= (1 - ExtendedDiscountCalculator.VIP_DISCOUNT)
        
        return max(0.0, final)
```

### Discount Analytics

```python
class DiscountAnalytics:
    def __init__(self):
        self.calculations = []
    
    def calculate_and_track(self, amount, customer_type):
        final = DiscountCalculator.calculate_discount(amount, customer_type)
        discount = amount - final
        
        self.calculations.append({
            "amount": amount,
            "customer_type": customer_type,
            "discount": discount,
            "final": final
        })
        
        return final
    
    def get_statistics(self):
        if not self.calculations:
            return {}
        
        total_discounts = sum(c["discount"] for c in self.calculations)
        avg_discount = total_discounts / len(self.calculations)
        
        return {
            "total_calculations": len(self.calculations),
            "total_discounts_given": total_discounts,
            "average_discount": avg_discount
        }
```

---

## FAQ

### Q1: What happens if I pass a negative amount?
**A**: The calculator will process it, but the final amount is guaranteed to be non-negative (minimum 0.0).

### Q2: Are customer types case-sensitive?
**A**: No, the calculator uses case-insensitive comparison. "PREMIUM", "premium", and "Premium" are all treated the same.

### Q3: What discount do I get for unknown customer types?
**A**: Unknown customer types receive 0% discount, but high-value purchase bonuses still apply.

### Q4: Can I modify the discount rates?
**A**: The class constants can be modified, but it's recommended to extend the class instead:

```python
class CustomDiscountCalculator(DiscountCalculator):
    PREMIUM_DISCOUNT = 0.25  # 25% instead of 20%
```

### Q5: Is this thread-safe?
**A**: Yes, the calculator uses static methods with no shared state, making it thread-safe.

### Q6: Can I use this with decimal amounts?
**A**: Yes, the calculator works with any float value, including decimal amounts.

---

## Support and Contribution

For issues, questions, or contributions:
- Review the MIGRATION_REPORT.md for technical details
- Check the inline code documentation
- Consult this usage guide

---

**Last Updated**: 2024
**Version**: 1.0
**Python Version**: 3.6+
