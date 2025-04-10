from datetime import datetime
from decimal import Decimal
from entity.customer import Customer

class Order:
    def __init__(self, order_id: int, customer: Customer, order_date: datetime, total_amount: Decimal):
        self.order_id = order_id
        self.customer = customer
        self.order_date = order_date
        self.total_amount = total_amount

    @property
    def order_id(self):
        return self._order_id

    @order_id.setter
    def order_id(self, value):
        if isinstance(value, int) and value > 0:
            self._order_id = value
        else:
            raise ValueError("Order ID must be a positive integer")

    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, value):
        if isinstance(value, Customer):
            self._customer = value
        else:
            raise ValueError("Customer must be a valid Customer instance")

    @property
    def order_date(self):
        return self._order_date

    @order_date.setter
    def order_date(self, value):
        if isinstance(value, datetime):
            self._order_date = value
        else:
            raise ValueError("Order date must be a datetime object")

    @property
    def total_amount(self):
        return self._total_amount

    @total_amount.setter
    def total_amount(self, value):
        if isinstance(value, Decimal) and value >= 0:
            self._total_amount = value
        else:
            raise ValueError("Total amount must be a non-negative Decimal")