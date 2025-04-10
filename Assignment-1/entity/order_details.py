from entity.orders import Order
from entity.products import Product

class OrderDetail:
    def __init__(self, order_detail_id: int, order: Order, product: Product, quantity: int):
        self.order_detail_id = order_detail_id
        self.order = order
        self.product = product
        self.quantity = quantity

    @property
    def order_detail_id(self):
        return self._order_detail_id

    @order_detail_id.setter
    def order_detail_id(self, value):
        if isinstance(value, int) and value > 0:
            self._order_detail_id = value
        else:
            raise ValueError("OrderDetail ID must be a positive integer")

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        if isinstance(value, Order):
            self._order = value
        else:
            raise ValueError("Order must be a valid Order instance")

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
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if isinstance(value, int) and value > 0:
            self._quantity = value
        else:
            raise ValueError("Quantity must be a positive integer")