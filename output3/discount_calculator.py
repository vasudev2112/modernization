"""Discount Calculator Module

This module provides functionality to calculate discounts based on customer type
and purchase amount.
"""


class DiscountCalculator:
    """A class to handle discount calculations for different customer types."""

    # Customer type constants
    PREMIUM = "PREMIUM"
    STANDARD = "STANDARD"

    # Discount rates
    PREMIUM_DISCOUNT = 0.20
    STANDARD_DISCOUNT = 0.10
    HIGH_VALUE_ADDITIONAL_DISCOUNT = 0.05
    HIGH_VALUE_THRESHOLD = 10000

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
            discount = DiscountCalculator.PREMIUM_DISCOUNT
        elif customer_type.upper() == DiscountCalculator.STANDARD:
            discount = DiscountCalculator.STANDARD_DISCOUNT

        # High-value purchase additional discount
        if amount > DiscountCalculator.HIGH_VALUE_THRESHOLD:
            discount += DiscountCalculator.HIGH_VALUE_ADDITIONAL_DISCOUNT

        # Calculate final amount
        final_amount = amount - (amount * discount)

        # Final amount should never be negative
        if final_amount < 0:
            final_amount = 0.0

        return final_amount


def main():
    """Sample execution demonstrating the discount calculator functionality."""
    # Test cases
    print(f"Premium customer with $5000 purchase: ${DiscountCalculator.calculate_discount(5000, 'PREMIUM')}")
    print(f"Standard customer with $15000 purchase: ${DiscountCalculator.calculate_discount(15000, 'STANDARD')}")
    print(f"Unknown customer type with $2000 purchase: ${DiscountCalculator.calculate_discount(2000, 'UNKNOWN')}")


if __name__ == "__main__":
    main()
