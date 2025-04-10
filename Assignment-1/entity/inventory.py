from datetime import datetime
from entity.products import Product

class Inventory:
    def __init__(self, inventory_id: int, product: Product, quantity_in_stock: int, last_stock_update: datetime):
        self.inventory_id = inventory_id
        self.product = product
        self.quantity_in_stock = quantity_in_stock
        self.last_stock_update = last_stock_update

    @property
    def inventory_id(self):
        return self._inventory_id

    @inventory_id.setter
    def inventory_id(self, value):
        if isinstance(value, int) and value > 0:
            self._inventory_id = value
        else:
            raise ValueError("Inventory ID must be a positive integer")

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, value):
        if isinstance(value, Product):
            self._product = value
        else:
            raise ValueError("Product must be a valid Product instance")

    @property
    def quantity_in_stock(self):
        return self._quantity_in_stock

    @quantity_in_stock.setter
    def quantity_in_stock(self, value):
        if isinstance(value, int) and value >= 0:
            self._quantity_in_stock = value
        else:
            raise ValueError("Quantity in stock must be a non-negative integer")

    @property
    def last_stock_update(self):
        return self._last_stock_update

    @last_stock_update.setter
    def last_stock_update(self, value):
        if isinstance(value, datetime):
            self._last_stock_update = value
        else:
            raise ValueError("Last stock update must be a datetime object")