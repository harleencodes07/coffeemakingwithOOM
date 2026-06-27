from math import isfinite


class MoneyMachine:
    """Models the machine that handles payments."""

    CURRENCY = "$"

    def __init__(self):
        self.profit = 0.0

    def report(self):
        """
        Returns the total profit.
        """
        return self.profit

    def get_profit(self):
        """
        Returns the current profit.
        """
        return self.profit

    def make_payment(self, amount_paid, cost):
        """
        Processes the payment.

        Parameters:
            amount_paid (float): Money inserted by the customer.
            cost (float): Cost of the selected drink.

        Returns:
            (True, change, message)
            or
            (False, shortage, message)
        """
        if not isfinite(amount_paid):
            raise ValueError("Amount paid must be a valid number.")

        if amount_paid < 0:
            raise ValueError("Amount paid cannot be negative.")

        if not isfinite(cost) or cost <= 0:
            raise ValueError("Cost must be greater than zero.")

        if amount_paid >= cost:
            change = round(amount_paid - cost, 2)
            self.profit += cost

            return (
                True,
                change,
                f"Payment successful! Change: ${change:.2f}"
            )

        shortage = round(cost - amount_paid, 2)

        return (
            False,
            shortage,
            f"Insufficient payment. You need ${shortage:.2f} more."
        )
