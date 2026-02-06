"""Discount Calculator Module

This module provides functionality to calculate discounts based on customer type
and purchase amount.
"""

from typing import Optional


def calculate_discount(amount: float, customer_type: str) -> float:
    """
    Calculates the final amount after applying discounts.

    Args:
        amount (float): Original purchase amount
        customer_type (str): Type of customer (PREMIUM or STANDARD)

    Returns:
        float: Final amount after discount

    Examples:
        >>> calculate_discount(5000, "PREMIUM")
        4000.0
        >>> calculate_discount(15000, "STANDARD")
        12750.0
        >>> calculate_discount(2000, "UNKNOWN")
        2000.0
    """
    discount = 0.0

    # Customer-based discount
    customer_type_upper = customer_type.upper()
    if customer_type_upper == "PREMIUM":
        discount = 0.20
    elif customer_type_upper == "STANDARD":
        discount = 0.10

    # High-value purchase additional discount
    if amount > 10000:
        discount += 0.05

    final_amount = amount - (amount * discount)

    # Final amount should never be negative
    if final_amount < 0:
        final_amount = 0.0

    return final_amount


if __name__ == "__main__":
    # Sample execution
    print(calculate_discount(5000, "PREMIUM"))    # 4000.0
    print(calculate_discount(15000, "STANDARD"))  # 12750.0
    print(calculate_discount(2000, "UNKNOWN"))    # 2000.0
