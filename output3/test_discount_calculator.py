"""Unit tests for the DiscountCalculator module.

This module contains comprehensive unit tests for the DiscountCalculator class,
ensuring all discount calculation logic works correctly.

To run tests:
    pip install pytest
    pytest test_discount_calculator.py -v
"""

import pytest
from discount_calculator import DiscountCalculator


class TestDiscountCalculator:
    """Test suite for DiscountCalculator class."""

    # Test Premium Customer Discounts
    def test_premium_customer_regular_purchase(self):
        """Test premium customer with regular purchase (< $10,000)."""
        result = DiscountCalculator.calculate_discount(5000, "PREMIUM")
        expected = 4000.0  # 20% discount
        assert result == expected, f"Expected {expected}, got {result}"

    def test_premium_customer_high_value_purchase(self):
        """Test premium customer with high-value purchase (> $10,000)."""
        result = DiscountCalculator.calculate_discount(12000, "PREMIUM")
        expected = 9000.0  # 20% + 5% = 25% discount
        assert result == expected, f"Expected {expected}, got {result}"

    def test_premium_customer_exact_threshold(self):
        """Test premium customer at exact high-value threshold."""
        result = DiscountCalculator.calculate_discount(10000, "PREMIUM")
        expected = 8000.0  # Only 20% discount (threshold not exceeded)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_premium_customer_just_over_threshold(self):
        """Test premium customer just over high-value threshold."""
        result = DiscountCalculator.calculate_discount(10001, "PREMIUM")
        expected = 7500.75  # 20% + 5% = 25% discount
        assert result == expected, f"Expected {expected}, got {result}"

    # Test Standard Customer Discounts
    def test_standard_customer_regular_purchase(self):
        """Test standard customer with regular purchase (< $10,000)."""
        result = DiscountCalculator.calculate_discount(5000, "STANDARD")
        expected = 4500.0  # 10% discount
        assert result == expected, f"Expected {expected}, got {result}"

    def test_standard_customer_high_value_purchase(self):
        """Test standard customer with high-value purchase (> $10,000)."""
        result = DiscountCalculator.calculate_discount(15000, "STANDARD")
        expected = 12750.0  # 10% + 5% = 15% discount
        assert result == expected, f"Expected {expected}, got {result}"

    def test_standard_customer_exact_threshold(self):
        """Test standard customer at exact high-value threshold."""
        result = DiscountCalculator.calculate_discount(10000, "STANDARD")
        expected = 9000.0  # Only 10% discount
        assert result == expected, f"Expected {expected}, got {result}"

    # Test Unknown/Other Customer Types
    def test_unknown_customer_regular_purchase(self):
        """Test unknown customer type with regular purchase."""
        result = DiscountCalculator.calculate_discount(2000, "UNKNOWN")
        expected = 2000.0  # No discount
        assert result == expected, f"Expected {expected}, got {result}"

    def test_unknown_customer_high_value_purchase(self):
        """Test unknown customer type with high-value purchase."""
        result = DiscountCalculator.calculate_discount(15000, "GUEST")
        expected = 14250.0  # Only 5% high-value discount
        assert result == expected, f"Expected {expected}, got {result}"

    def test_empty_customer_type(self):
        """Test with empty customer type string."""
        result = DiscountCalculator.calculate_discount(5000, "")
        expected = 5000.0  # No discount
        assert result == expected, f"Expected {expected}, got {result}"

    # Test Case Sensitivity
    def test_premium_lowercase(self):
        """Test premium customer type in lowercase."""
        result = DiscountCalculator.calculate_discount(5000, "premium")
        expected = 4000.0  # Should work case-insensitively
        assert result == expected, f"Expected {expected}, got {result}"

    def test_standard_mixed_case(self):
        """Test standard customer type in mixed case."""
        result = DiscountCalculator.calculate_discount(5000, "StAnDaRd")
        expected = 4500.0  # Should work case-insensitively
        assert result == expected, f"Expected {expected}, got {result}"

    def test_premium_with_spaces(self):
        """Test premium customer type with leading/trailing spaces."""
        # Note: Current implementation doesn't strip spaces
        # This test documents current behavior
        result = DiscountCalculator.calculate_discount(5000, " PREMIUM ")
        expected = 5000.0  # Spaces cause no match, no discount
        assert result == expected, f"Expected {expected}, got {result}"

    # Test Edge Cases
    def test_zero_amount(self):
        """Test with zero purchase amount."""
        result = DiscountCalculator.calculate_discount(0, "PREMIUM")
        expected = 0.0
        assert result == expected, f"Expected {expected}, got {result}"

    def test_very_small_amount(self):
        """Test with very small purchase amount."""
        result = DiscountCalculator.calculate_discount(0.01, "PREMIUM")
        expected = 0.008  # 20% discount
        assert abs(result - expected) < 0.0001, f"Expected {expected}, got {result}"

    def test_very_large_amount(self):
        """Test with very large purchase amount."""
        result = DiscountCalculator.calculate_discount(1000000, "PREMIUM")
        expected = 750000.0  # 25% discount (20% + 5%)
        assert result == expected, f"Expected {expected}, got {result}"

    def test_negative_amount_protection(self):
        """Test that negative amounts are handled correctly."""
        # Note: Current implementation doesn't validate input
        # but ensures output is non-negative
        result = DiscountCalculator.calculate_discount(-1000, "PREMIUM")
        expected = 0.0  # Should be protected to 0
        assert result >= 0, f"Result should be non-negative, got {result}"

    # Test Discount Calculation Accuracy
    def test_discount_calculation_precision(self):
        """Test discount calculation with decimal precision."""
        result = DiscountCalculator.calculate_discount(1234.56, "PREMIUM")
        expected = 987.648  # 20% discount
        assert abs(result - expected) < 0.001, f"Expected {expected}, got {result}"

    def test_combined_discount_calculation(self):
        """Test combined discount calculation (base + high-value)."""
        result = DiscountCalculator.calculate_discount(20000, "STANDARD")
        # 10% + 5% = 15% discount
        # 20000 * 0.15 = 3000
        # 20000 - 3000 = 17000
        expected = 17000.0
        assert result == expected, f"Expected {expected}, got {result}"

    # Test Class Constants
    def test_premium_constant(self):
        """Test PREMIUM constant is correctly defined."""
        assert DiscountCalculator.PREMIUM == "PREMIUM"

    def test_standard_constant(self):
        """Test STANDARD constant is correctly defined."""
        assert DiscountCalculator.STANDARD == "STANDARD"

    def test_premium_discount_rate(self):
        """Test PREMIUM_DISCOUNT rate is correctly defined."""
        assert DiscountCalculator.PREMIUM_DISCOUNT == 0.20

    def test_standard_discount_rate(self):
        """Test STANDARD_DISCOUNT rate is correctly defined."""
        assert DiscountCalculator.STANDARD_DISCOUNT == 0.10

    def test_high_value_additional_discount_rate(self):
        """Test HIGH_VALUE_ADDITIONAL_DISCOUNT rate is correctly defined."""
        assert DiscountCalculator.HIGH_VALUE_ADDITIONAL_DISCOUNT == 0.05

    def test_high_value_threshold(self):
        """Test HIGH_VALUE_THRESHOLD is correctly defined."""
        assert DiscountCalculator.HIGH_VALUE_THRESHOLD == 10000

    # Parametrized Tests
    @pytest.mark.parametrize("amount,customer_type,expected", [
        (5000, "PREMIUM", 4000.0),
        (15000, "STANDARD", 12750.0),
        (2000, "UNKNOWN", 2000.0),
        (12000, "PREMIUM", 9000.0),
        (10001, "STANDARD", 8500.85),
        (0, "PREMIUM", 0.0),
        (100, "STANDARD", 90.0),
    ])
    def test_various_scenarios(self, amount, customer_type, expected):
        """Test various discount scenarios with parametrized inputs."""
        result = DiscountCalculator.calculate_discount(amount, customer_type)
        assert abs(result - expected) < 0.01, f"For {amount} and {customer_type}, expected {expected}, got {result}"


class TestDiscountCalculatorIntegration:
    """Integration tests for DiscountCalculator."""

    def test_multiple_calculations(self):
        """Test multiple sequential calculations."""
        results = [
            DiscountCalculator.calculate_discount(5000, "PREMIUM"),
            DiscountCalculator.calculate_discount(15000, "STANDARD"),
            DiscountCalculator.calculate_discount(2000, "GUEST"),
        ]
        expected = [4000.0, 12750.0, 2000.0]
        assert results == expected, f"Expected {expected}, got {results}"

    def test_batch_processing(self):
        """Test batch processing of multiple orders."""
        orders = [
            (5000, "PREMIUM"),
            (15000, "STANDARD"),
            (2000, "GUEST"),
            (12000, "PREMIUM"),
        ]
        
        results = []
        for amount, customer_type in orders:
            result = DiscountCalculator.calculate_discount(amount, customer_type)
            results.append(result)
        
        expected = [4000.0, 12750.0, 2000.0, 9000.0]
        assert results == expected, f"Expected {expected}, got {results}"

    def test_total_savings_calculation(self):
        """Test calculating total savings across multiple orders."""
        orders = [
            (5000, "PREMIUM"),
            (15000, "STANDARD"),
            (12000, "PREMIUM"),
        ]
        
        total_original = sum(amount for amount, _ in orders)
        total_final = sum(
            DiscountCalculator.calculate_discount(amount, customer_type)
            for amount, customer_type in orders
        )
        total_savings = total_original - total_final
        
        expected_savings = 1000 + 2250 + 3000  # Individual savings
        assert abs(total_savings - expected_savings) < 0.01, \
            f"Expected savings {expected_savings}, got {total_savings}"


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise run basic tests
    try:
        import sys
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not installed. Running basic tests...")
        print("Install pytest with: pip install pytest")
        print("\nRunning basic validation...")
        
        # Basic validation tests
        test = TestDiscountCalculator()
        test.test_premium_customer_regular_purchase()
        test.test_standard_customer_high_value_purchase()
        test.test_unknown_customer_regular_purchase()
        
        print("✅ Basic validation tests passed!")
        print("For comprehensive testing, install pytest and run: pytest test_discount_calculator.py -v")
