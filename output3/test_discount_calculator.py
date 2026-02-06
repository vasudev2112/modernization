"""Unit tests for the Discount Calculator module.

This test suite provides comprehensive coverage of the DiscountCalculator class,
including edge cases, boundary conditions, and various customer scenarios.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path if needed
sys.path.insert(0, str(Path(__file__).parent))

from discount_calculator import DiscountCalculator


class TestDiscountCalculatorBasic:
    """Basic functionality tests for DiscountCalculator."""

    def test_premium_customer_standard_amount(self):
        """Test premium customer with standard purchase amount."""
        result = DiscountCalculator.calculate_discount(5000, "PREMIUM")
        assert result == 4000.0, "Premium customer should get 20% discount on $5000"

    def test_standard_customer_standard_amount(self):
        """Test standard customer with standard purchase amount."""
        result = DiscountCalculator.calculate_discount(5000, "STANDARD")
        assert result == 4500.0, "Standard customer should get 10% discount on $5000"

    def test_premium_customer_high_value(self):
        """Test premium customer with high-value purchase."""
        result = DiscountCalculator.calculate_discount(15000, "PREMIUM")
        expected = 11250.0  # 25% discount (20% + 5%)
        assert result == expected, "Premium customer should get 25% discount on $15000"

    def test_standard_customer_high_value(self):
        """Test standard customer with high-value purchase."""
        result = DiscountCalculator.calculate_discount(15000, "STANDARD")
        expected = 12750.0  # 15% discount (10% + 5%)
        assert result == expected, "Standard customer should get 15% discount on $15000"

    def test_unknown_customer_type(self):
        """Test unknown customer type receives no discount."""
        result = DiscountCalculator.calculate_discount(2000, "UNKNOWN")
        assert result == 2000.0, "Unknown customer type should receive no discount"


class TestDiscountCalculatorCaseSensitivity:
    """Test case-insensitive customer type handling."""

    @pytest.mark.parametrize("customer_type", [
        "PREMIUM",
        "premium",
        "Premium",
        "PrEmIuM",
    ])
    def test_premium_case_insensitive(self, customer_type):
        """Test that customer type is case-insensitive for premium."""
        result = DiscountCalculator.calculate_discount(5000, customer_type)
        assert result == 4000.0

    @pytest.mark.parametrize("customer_type", [
        "STANDARD",
        "standard",
        "Standard",
        "StAnDaRd",
    ])
    def test_standard_case_insensitive(self, customer_type):
        """Test that customer type is case-insensitive for standard."""
        result = DiscountCalculator.calculate_discount(5000, customer_type)
        assert result == 4500.0


class TestDiscountCalculatorEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_zero_amount(self):
        """Test zero purchase amount."""
        result = DiscountCalculator.calculate_discount(0, "PREMIUM")
        assert result == 0.0, "Zero amount should result in zero"

    def test_negative_amount(self):
        """Test negative amount protection."""
        result = DiscountCalculator.calculate_discount(-100, "PREMIUM")
        assert result == 0.0, "Negative final amount should be converted to zero"

    def test_exactly_at_threshold(self):
        """Test amount exactly at high-value threshold."""
        result = DiscountCalculator.calculate_discount(10000, "STANDARD")
        expected = 9000.0  # Only 10% discount, not high-value yet
        assert result == expected, "Amount at threshold should not get high-value discount"

    def test_just_above_threshold(self):
        """Test amount just above high-value threshold."""
        result = DiscountCalculator.calculate_discount(10001, "STANDARD")
        expected = 8500.85  # 15% discount (10% + 5%)
        assert pytest.approx(result, rel=1e-9) == expected

    def test_just_below_threshold(self):
        """Test amount just below high-value threshold."""
        result = DiscountCalculator.calculate_discount(9999, "STANDARD")
        expected = 8999.1  # Only 10% discount
        assert pytest.approx(result, rel=1e-9) == expected

    def test_very_large_amount(self):
        """Test very large purchase amount."""
        result = DiscountCalculator.calculate_discount(1000000, "PREMIUM")
        expected = 750000.0  # 25% discount
        assert result == expected

    def test_very_small_amount(self):
        """Test very small purchase amount."""
        result = DiscountCalculator.calculate_discount(0.01, "PREMIUM")
        expected = 0.008  # 20% discount
        assert pytest.approx(result, rel=1e-9) == expected


class TestDiscountCalculatorParametrized:
    """Parametrized tests for comprehensive coverage."""

    @pytest.mark.parametrize("amount,customer_type,expected", [
        # Premium customers - standard amounts
        (1000, "PREMIUM", 800.0),
        (5000, "PREMIUM", 4000.0),
        (10000, "PREMIUM", 8000.0),
        
        # Premium customers - high-value amounts
        (10001, "PREMIUM", 7500.75),
        (15000, "PREMIUM", 11250.0),
        (20000, "PREMIUM", 15000.0),
        
        # Standard customers - standard amounts
        (1000, "STANDARD", 900.0),
        (5000, "STANDARD", 4500.0),
        (10000, "STANDARD", 9000.0),
        
        # Standard customers - high-value amounts
        (10001, "STANDARD", 8500.85),
        (15000, "STANDARD", 12750.0),
        (20000, "STANDARD", 17000.0),
        
        # Unknown customer types
        (1000, "UNKNOWN", 1000.0),
        (5000, "GOLD", 5000.0),
        (10000, "VIP", 10000.0),
        (15000, "", 15000.0),
        
        # Edge cases
        (0, "PREMIUM", 0.0),
        (0, "STANDARD", 0.0),
        (0.01, "PREMIUM", 0.008),
    ])
    def test_various_scenarios(self, amount, customer_type, expected):
        """Test various amount and customer type combinations."""
        result = DiscountCalculator.calculate_discount(amount, customer_type)
        assert pytest.approx(result, rel=1e-9) == expected


class TestDiscountCalculatorConstants:
    """Test that class constants are properly defined."""

    def test_customer_type_constants_exist(self):
        """Test that customer type constants are defined."""
        assert hasattr(DiscountCalculator, 'PREMIUM')
        assert hasattr(DiscountCalculator, 'STANDARD')
        assert DiscountCalculator.PREMIUM == "PREMIUM"
        assert DiscountCalculator.STANDARD == "STANDARD"

    def test_discount_rate_constants_exist(self):
        """Test that discount rate constants are defined."""
        assert hasattr(DiscountCalculator, 'PREMIUM_DISCOUNT')
        assert hasattr(DiscountCalculator, 'STANDARD_DISCOUNT')
        assert hasattr(DiscountCalculator, 'HIGH_VALUE_DISCOUNT')
        assert DiscountCalculator.PREMIUM_DISCOUNT == 0.20
        assert DiscountCalculator.STANDARD_DISCOUNT == 0.10
        assert DiscountCalculator.HIGH_VALUE_DISCOUNT == 0.05

    def test_threshold_constant_exists(self):
        """Test that high-value threshold constant is defined."""
        assert hasattr(DiscountCalculator, 'HIGH_VALUE_THRESHOLD')
        assert DiscountCalculator.HIGH_VALUE_THRESHOLD == 10000


class TestDiscountCalculatorDocumentation:
    """Test that proper documentation exists."""

    def test_class_has_docstring(self):
        """Test that the class has a docstring."""
        assert DiscountCalculator.__doc__ is not None
        assert len(DiscountCalculator.__doc__.strip()) > 0

    def test_method_has_docstring(self):
        """Test that calculate_discount method has a docstring."""
        assert DiscountCalculator.calculate_discount.__doc__ is not None
        assert len(DiscountCalculator.calculate_discount.__doc__.strip()) > 0

    def test_method_has_type_hints(self):
        """Test that calculate_discount has type hints."""
        annotations = DiscountCalculator.calculate_discount.__annotations__
        assert 'amount' in annotations
        assert 'customer_type' in annotations
        assert 'return' in annotations


class TestDiscountCalculatorIntegration:
    """Integration tests simulating real-world usage."""

    def test_batch_processing(self):
        """Test processing multiple discount calculations."""
        test_cases = [
            (5000, "PREMIUM", 4000.0),
            (15000, "STANDARD", 12750.0),
            (2000, "UNKNOWN", 2000.0),
        ]
        
        for amount, customer_type, expected in test_cases:
            result = DiscountCalculator.calculate_discount(amount, customer_type)
            assert result == expected

    def test_realistic_shopping_cart(self):
        """Test realistic shopping cart scenario."""
        # Customer adds items to cart
        cart_total = 8500.00
        customer_type = "PREMIUM"
        
        # Calculate final amount
        final_amount = DiscountCalculator.calculate_discount(cart_total, customer_type)
        
        # Verify discount applied correctly
        expected = 6800.0  # 20% discount
        assert final_amount == expected
        
        # Verify discount amount
        discount_amount = cart_total - final_amount
        assert discount_amount == 1700.0

    def test_high_value_purchase_scenario(self):
        """Test high-value purchase with additional discount."""
        # Large purchase
        cart_total = 25000.00
        customer_type = "STANDARD"
        
        # Calculate final amount
        final_amount = DiscountCalculator.calculate_discount(cart_total, customer_type)
        
        # Should get 15% total discount (10% + 5%)
        expected = 21250.0
        assert final_amount == expected
        
        # Verify total savings
        savings = cart_total - final_amount
        assert savings == 3750.0


class TestDiscountCalculatorPerformance:
    """Performance-related tests."""

    def test_calculation_speed(self):
        """Test that calculations are fast enough."""
        import time
        
        start_time = time.time()
        
        # Perform 10000 calculations
        for _ in range(10000):
            DiscountCalculator.calculate_discount(5000, "PREMIUM")
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should complete in less than 1 second
        assert elapsed < 1.0, f"10000 calculations took {elapsed:.2f} seconds"


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
