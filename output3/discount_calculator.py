"""Discount Calculator Module

This module provides functionality to calculate discounts based on customer type
and purchase amount.

Author: Automated Java to Python Migration Agent
Date: 2024
"""

from typing import Union


class DiscountCalculator:
    """A class to handle discount calculations for different customer types."""

    # Customer type constants
    PREMIUM = "PREMIUM"
    STANDARD = "STANDARD"

    @staticmethod
    def calculate_discount(amount: float, customer_type: str) -> float:
        """
        Calculates the final amount after applying discounts.

        Args:
            amount (float): Original purchase amount
            customer_type (str): Type of customer (PREMIUM or STANDARD)

        Returns:
            float: Final amount after discount

        Examples:
            >>> DiscountCalculator.calculate_discount(5000, "PREMIUM")
            4000.0
            >>> DiscountCalculator.calculate_discount(15000, "STANDARD")
            12750.0
            >>> DiscountCalculator.calculate_discount(2000, "UNKNOWN")
            2000.0
        """
        discount = 0.0

        # Customer-based discount
        if customer_type.upper() == DiscountCalculator.PREMIUM:
            discount = 0.20
        elif customer_type.upper() == DiscountCalculator.STANDARD:
            discount = 0.10

        # High-value purchase additional discount
        if amount > 10000:
            discount += 0.05

        final_amount = amount - (amount * discount)

        # Final amount should never be negative
        if final_amount < 0:
            final_amount = 0.0

        return final_amount


def main():
    """Sample execution demonstrating the discount calculator functionality."""
    # Test cases
    print(f"Premium customer, $5000 purchase: ${DiscountCalculator.calculate_discount(5000, 'PREMIUM')}")
    print(f"Standard customer, $15000 purchase: ${DiscountCalculator.calculate_discount(15000, 'STANDARD')}")
    print(f"Unknown customer type, $2000 purchase: ${DiscountCalculator.calculate_discount(2000, 'UNKNOWN')}")


if __name__ == "__main__":
    main()
