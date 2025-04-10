class Product:
    def __init__(self, product_id, product_name, description, price):
        self.product_id = product_id
        self.product_name = product_name
        self.description = description
        self.price = price

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, value):
        if isinstance(value, int) and value > 0:
            self._product_id = value
        else:
            raise ValueError("Product ID must be a positive integer")

    @property
    def product_name(self):
        return self._product_name

    @product_name.setter
    def product_name(self, value):
        if isinstance(value, str) and value.strip():
            self._product_name = value
        else:
            raise ValueError("Product name must be a non-empty string")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, str):
            self._description = value
        else:
            raise ValueError("Description must be a string")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if isinstance(value, (int, float)) and value >= 0:
            self._price = float(value)
        else:
            raise ValueError("Price must be a non-negative number")