class CoffeeMaker:
    """Models the machine that makes the coffee."""

    def __init__(self):
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
        }

    def report(self):
        """Returns the current resources."""
        return self.resources.copy()

    def get_resources(self):
        """Returns a copy of the current resources."""
        return self.resources.copy()

    def is_resource_sufficient(self, drink):
        """
        Returns (True, message) when resources are available, otherwise
        returns (False, reason).
        """
        for item, required_amount in drink.ingredients.items():
            if required_amount > self.resources[item]:
                return False, f"Not enough {item}."

        return True, "Resources available."

    def make_coffee(self, order):
        """Deducts the ingredients for an order and returns a success message."""
        available, message = self.is_resource_sufficient(order)
        if not available:
            raise ValueError(message)

        for item, required_amount in order.ingredients.items():
            self.resources[item] -= required_amount

        return f"Enjoy your {order.name}!"

    def refill(self, water, milk, coffee):
        """Refills the machine with non-negative whole-number amounts."""
        amounts = {"water": water, "milk": milk, "coffee": coffee}
        for item, amount in amounts.items():
            if not isinstance(amount, int):
                raise ValueError(f"{item.title()} must be a whole number.")
            if amount < 0:
                raise ValueError(f"{item.title()} cannot be negative.")

        if water == 0 and milk == 0 and coffee == 0:
            raise ValueError("Enter at least one amount to refill.")

        self.resources["water"] += water
        self.resources["milk"] += milk
        self.resources["coffee"] += coffee

        return "Machine refilled successfully!"
