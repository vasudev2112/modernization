"""Unit tests for DiscountCalculator module.

This test suite validates the functionality of the DiscountCalculator class,
ensuring functional equivalence with the original Java implementation.
"""

import pytest
from discount_calculator import DiscountCalculator


class TestDiscountCalculatorBasic:
    """Basic functionality tests for DiscountCalculator."""

    def test_premium_customer_standard_amount(self):
        """Test premium customer with amount <= 10000."""
        result = DiscountCalculator.calculate_discount(5000, "PREMIUM")
        assert result == 4000.0, "Premium customer should get 20% discount"

    def test_standard_customer_standard_amount(self):
        """Test standard customer with amount <= 10000."""
        result = DiscountCalculator.calculate_discount(5000, "STANDARD")
        assert result == 4500.0, "Standard customer should get 10% discount"

    def test_standard_customer_high_amount(self):
        """Test standard customer with amount > 10000."""
        result = DiscountCalculator.calculate_discount(15000, "STANDARD")
        assert result == 12750.0, "Standard customer with high amount should get 15% total discount"

    def test_unknown_customer_type(self):
        """Test unknown customer type with no discount."""
        result = DiscountCalculator.calculate_discount(2000, "UNKNOWN")
        assert result == 2000.0, "Unknown customer should get no discount"

    def test_premium_customer_high_amount(self):
        """Test premium customer with amount > 10000."""
        result = DiscountCalculator.calculate_discount(15000, "PREMIUM")
        assert result == 11250.0, "Premium customer with high amount should get 25% total discount"


class TestDiscountCalculatorEdgeCases:
    """Edge case tests for DiscountCalculator."""

    def test_zero_amount(self):
        """Test with zero amount."""
        result = DiscountCalculator.calculate_discount(0, "PREMIUM")
        assert result == 0.0, "Zero amount should return zero"

    def test_very_small_amount(self):
        """Test with very small amount."""
        result = DiscountCalculator.calculate_discount(0.01, "PREMIUM")
        assert result == 0.008, "Small amounts should be calculated correctly"

    def test_exactly_threshold_amount(self):
        """Test with amount exactly at threshold (10000)."""
        result = DiscountCalculator.calculate_discount(10000, "PREMIUM")
        assert result == 8000.0, "Amount at threshold should not get high-value discount"

    def test_just_above_threshold(self):
        """Test with amount just above threshold (10000.01)."""
        result = DiscountCalculator.calculate_discount(10000.01, "PREMIUM")
        expected = 10000.01 * 0.75  # 25% discount
        assert abs(result - expected) < 0.01, "Amount just above threshold should get high-value discount"

    def test_very_large_amount(self):
        """Test with very large amount."""
        result = DiscountCalculator.calculate_discount(1000000, "PREMIUM")
        assert result == 750000.0, "Large amounts should be calculated correctly"

    def test_negative_amount_protection(self):
        """Test that negative final amounts are prevented."""
        # Even with maximum discount, result should not be negative
        result = DiscountCalculator.calculate_discount(100, "PREMIUM")
        assert result >= 0, "Final amount should never be negative"


class TestDiscountCalculatorCaseInsensitivity:
    """Tests for case-insensitive customer type handling."""

    def test_lowercase_premium(self):
        """Test lowercase 'premium'."""
        result = DiscountCalculator.calculate_discount(5000, "premium")
        assert result == 4000.0, "Lowercase 'premium' should work"

    def test_uppercase_premium(self):
        """Test uppercase 'PREMIUM'."""
        result = DiscountCalculator.calculate_discount(5000, "PREMIUM")
        assert result == 4000.0, "Uppercase 'PREMIUM' should work"

    def test_mixed_case_premium(self):
        """Test mixed case 'PrEmIuM'."""
        result = DiscountCalculator.calculate_discount(5000, "PrEmIuM")
        assert result == 4000.0, "Mixed case 'PrEmIuM' should work"

    def test_lowercase_standard(self):
        """Test lowercase 'standard'."""
        result = DiscountCalculator.calculate_discount(5000, "standard")
        assert result == 4500.0, "Lowercase 'standard' should work"

    def test_case_consistency(self):
        """Test that all case variations produce same result."""
        amount = 5000
        variations = ["PREMIUM", "premium", "Premium", "PrEmIuM"]
        results = [DiscountCalculator.calculate_discount(amount, var) for var in variations]
        assert all(r == results[0] for r in results), "All case variations should produce same result"


class TestDiscountCalculatorBusinessRules:
    """Tests for specific business rules and discount combinations."""

    def test_premium_base_discount_only(self):
        """Test premium customer gets 20% base discount only (amount <= 10000)."""
        amount = 5000
        result = DiscountCalculator.calculate_discount(amount, "PREMIUM")
        expected = amount * 0.80  # 20% discount
        assert result == expected, "Premium base discount should be 20%"

    def test_standard_base_discount_only(self):
        """Test standard customer gets 10% base discount only (amount <= 10000)."""
        amount = 5000
        result = DiscountCalculator.calculate_discount(amount, "STANDARD")
        expected = amount * 0.90  # 10% discount
        assert result == expected, "Standard base discount should be 10%"

    def test_premium_combined_discount(self):
        """Test premium customer gets 25% total discount (amount > 10000)."""
        amount = 15000
        result = DiscountCalculator.calculate_discount(amount, "PREMIUM")
        expected = amount * 0.75  # 20% + 5% = 25% discount
        assert result == expected, "Premium combined discount should be 25%"

    def test_standard_combined_discount(self):
        """Test standard customer gets 15% total discount (amount > 10000)."""
        amount = 15000
        result = DiscountCalculator.calculate_discount(amount, "STANDARD")
        expected = amount * 0.85  # 10% + 5% = 15% discount
        assert result == expected, "Standard combined discount should be 15%"

    def test_high_value_discount_only(self):
        """Test unknown customer gets only high-value discount (amount > 10000)."""
        amount = 15000
        result = DiscountCalculator.calculate_discount(amount, "UNKNOWN")
        expected = amount * 0.95  # 5% discount only
        assert result == expected, "Unknown customer should get only high-value discount"

    def test_no_discount_scenario(self):
        """Test scenario with no discounts applied."""
        amount = 5000
        result = DiscountCalculator.calculate_discount(amount, "UNKNOWN")
        assert result == amount, "Unknown customer with low amount should get no discount"


class TestDiscountCalculatorConstants:
    """Tests for class constants."""

    def test_premium_constant_exists(self):
        """Test PREMIUM constant exists."""
        assert hasattr(DiscountCalculator, "PREMIUM"), "PREMIUM constant should exist"

    def test_standard_constant_exists(self):
        """Test STANDARD constant exists."""
        assert hasattr(DiscountCalculator, "STANDARD"), "STANDARD constant should exist"

    def test_premium_constant_value(self):
        """Test PREMIUM constant has correct value."""
        assert DiscountCalculator.PREMIUM == "PREMIUM", "PREMIUM constant should be 'PREMIUM'"

    def test_standard_constant_value(self):
        """Test STANDARD constant has correct value."""
        assert DiscountCalculator.STANDARD == "STANDARD", "STANDARD constant should be 'STANDARD'"

    def test_using_constants(self):
        """Test that constants can be used in calculations."""
        result = DiscountCalculator.calculate_discount(5000, DiscountCalculator.PREMIUM)
        assert result == 4000.0, "Constants should work in calculations"


class TestDiscountCalculatorIntegration:
    """Integration tests matching original Java test cases."""

    def test_java_test_case_1(self):
        """Test case 1 from Java: calculateDiscount(5000, "PREMIUM") -> 4000."""
        result = DiscountCalculator.calculate_discount(5000, "PREMIUM")
        assert result == 4000.0, "Java test case 1 failed"

    def test_java_test_case_2(self):
        """Test case 2 from Java: calculateDiscount(15000, "STANDARD") -> 12750."""
        result = DiscountCalculator.calculate_discount(15000, "STANDARD")
        assert result == 12750.0, "Java test case 2 failed"

    def test_java_test_case_3(self):
        """Test case 3 from Java: calculateDiscount(2000, "UNKNOWN") -> 2000."""
        result = DiscountCalculator.calculate_discount(2000, "UNKNOWN")
        assert result == 2000.0, "Java test case 3 failed"

    def test_all_java_test_cases(self):
        """Test all Java test cases together."""
        test_cases = [
            (5000, "PREMIUM", 4000.0),
            (15000, "STANDARD", 12750.0),
            (2000, "UNKNOWN", 2000.0),
        ]
        
        for amount, customer_type, expected in test_cases:
            result = DiscountCalculator.calculate_discount(amount, customer_type)
            assert result == expected, f"Failed for {amount}, {customer_type}: expected {expected}, got {result}"


class TestDiscountCalculatorBatchProcessing:
    """Tests for batch processing scenarios."""

    def test_multiple_customers(self):
        """Test processing multiple customers."""
        customers = [
            (5000, "PREMIUM", 4000.0),
            (15000, "STANDARD", 12750.0),
            (2000, "STANDARD", 1800.0),
            (20000, "PREMIUM", 15000.0),
        ]
        
        for amount, customer_type, expected in customers:
            result = DiscountCalculator.calculate_discount(amount, customer_type)
            assert result == expected, f"Batch processing failed for {amount}, {customer_type}"

    def test_same_customer_multiple_purchases(self):
        """Test same customer type with different amounts."""
        amounts = [1000, 5000, 10000, 15000, 20000]
        customer_type = "PREMIUM"
        
        for amount in amounts:
            result = DiscountCalculator.calculate_discount(amount, customer_type)
            assert result >= 0, f"Failed for amount {amount}"
            assert result <= amount, f"Result should not exceed original amount for {amount}"


class TestDiscountCalculatorPrecision:
    """Tests for numerical precision and accuracy."""

    def test_decimal_precision(self):
        """Test that decimal calculations are precise."""
        result = DiscountCalculator.calculate_discount(1234.56, "PREMIUM")
        expected = 1234.56 * 0.80
        assert abs(result - expected) < 0.001, "Decimal precision should be maintained"

    def test_floating_point_accuracy(self):
        """Test floating point accuracy for various amounts."""
        test_amounts = [99.99, 1000.01, 10000.50, 15000.75]
        
        for amount in test_amounts:
            result = DiscountCalculator.calculate_discount(amount, "PREMIUM")
            # Result should be reasonable (between 0 and original amount)
            assert 0 <= result <= amount, f"Result out of range for amount {amount}"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
