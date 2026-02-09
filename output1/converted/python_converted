class DiscountCalculator:
    """
    Calculates the final amount after applying discounts.

    Methods
    -------
    calculate_discount(amount: float, customer_type: str) -> float
        Calculates the discounted amount based on customer type and purchase amount.
    """

    @staticmethod
    def calculate_discount(amount: float, customer_type: str) -> float:
        """
        Calculates the final amount after applying discounts.

        Parameters
        ----------
        amount : float
            Original purchase amount.
        customer_type : str
            Type of customer ('PREMIUM' or 'STANDARD').

        Returns
        -------
        float
            Final amount after discount.
        """
        discount = 0.0

        # Customer-based discount
        if customer_type.strip().upper() == "PREMIUM":
            discount = 0.20
        elif customer_type.strip().upper() == "STANDARD":
            discount = 0.10

        # High-value purchase additional discount
        if amount > 10000:
            discount += 0.05

        final_amount = amount - (amount * discount)

        # Final amount should never be negative
        if final_amount < 0:
            final_amount = 0.0

        return final_amount
