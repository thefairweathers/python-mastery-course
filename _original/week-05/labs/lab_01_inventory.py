"""
Lab 5.1: Inventory System — Build using dicts, sets, and defaultdict.
TODO: Implement the Inventory class (see Week 5 README for reference).
"""
from collections import defaultdict

class Inventory:
    def __init__(self):
        self.items = {}
        self.tag_index = defaultdict(set)

    def add_item(self, name, qty, price, tags=None):
        # TODO: Store item and update tag index
        pass

    def search_by_tags(self, *tags):
        # TODO: Return items matching ALL tags (set intersection)
        pass

    def total_value(self):
        # TODO: Sum of qty * price for all items
        pass

if __name__ == "__main__":
    inv = Inventory()
    inv.add_item("MacBook Pro", 5, 2499.00, ["electronics", "laptop"])
    inv.add_item("USB-C Hub", 50, 39.99, ["electronics", "accessory"])
    print("Total value:", inv.total_value())
    print("Electronics:", inv.search_by_tags("electronics"))
