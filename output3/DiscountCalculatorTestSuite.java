import static org.junit.Assert.*;
import org.junit.Test;

public class DiscountCalculatorTestSuite {
    @Test
    public void testPremiumCustomerNormalAmount() {
        assertEquals(4000.0, DiscountCalculator.calculateDiscount(5000, "PREMIUM"), 0.001);
    }

    @Test
    public void testStandardCustomerHighAmount() {
        assertEquals(12750.0, DiscountCalculator.calculateDiscount(15000, "STANDARD"), 0.001);
    }

    @Test
    public void testUnknownCustomerType() {
        assertEquals(2000.0, DiscountCalculator.calculateDiscount(2000, "UNKNOWN"), 0.001);
    }

    @Test
    public void testPremiumCustomerHighAmount() {
        assertEquals(9000.0, DiscountCalculator.calculateDiscount(12000, "PREMIUM"), 0.001);
    }

    @Test
    public void testNegativeAmount() {
        assertEquals(0.0, DiscountCalculator.calculateDiscount(-1000, "STANDARD"), 0.001);
    }

    @Test
    public void testZeroAmount() {
        assertEquals(0.0, DiscountCalculator.calculateDiscount(0, "PREMIUM"), 0.001);
    }
}
