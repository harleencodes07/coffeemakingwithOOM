class MenuItem:
    """Models each Menu Item."""

    def __init__(self, name, water, milk, coffee, cost):
        self.name = name
        self.cost = cost
        self.ingredients = {
            "water": water,
            "milk": milk,
            "coffee": coffee
        }


class Menu:
    """Models the Menu with drinks."""

    def __init__(self):
        self.menu = [
            MenuItem("latte", 200, 150, 24, 2.5),
            MenuItem("espresso", 50, 0, 18, 1.5),
            MenuItem("cappuccino", 250, 50, 24, 3.0),
        ]

    def get_items(self):
        """Returns a list of all drinks."""
        return [item.name for item in self.menu]

    def get_menu(self):
        """Returns the complete menu."""
        return self.menu

    def find_drink(self, order_name):
        """
        Searches the menu for a drink.
        Returns:
            (True, MenuItem)
        or
            (False, "Drink not found")
        """
        for item in self.menu:
            if item.name.lower() == order_name.lower():
                return True, item

        return False, "Sorry, that drink is not available."

    def get_drink_info(self, order_name):
        """
        Returns all information about a drink.
        """

        found, drink = self.find_drink(order_name)

        if found:
            return {
                "name": drink.name,
                "cost": drink.cost,
                "ingredients": drink.ingredients
            }

        return None