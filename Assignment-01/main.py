# TechShop Application Implementation
from datetime import datetime
from typing import List

# Task 1 & 2: Define classes with appropriate attributes and encapsulation
class Customer:
    def __init__(self, customer_id: int, first_name: str, last_name: str, email: str, phone: str, address: str):
        self.__customer_id = customer_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__phone = phone
        self.__address = address
        self.__orders = []

    @property
    def customer_id(self):
        return self.__customer_id

    def calculate_total_orders(self) -> int:
        return len(self.__orders)

    def get_customer_details(self) -> str:
        return f"Customer ID: {self.__customer_id}, Name: {self.__first_name} {self.__last_name}, Email: {self.__email}, Phone: {self.__phone}, Address: {self.__address}"

    def update_customer_info(self, email=None, phone=None, address=None):
        if email: self.__email = email
        if phone: self.__phone = phone
        if address: self.__address = address

    def add_order(self, order):
        self.__orders.append(order)


class Product:
    def __init__(self, product_id: int, name: str, description: str, price: float):
        self.__product_id = product_id
        self.__name = name
        self.__description = description
        self.__price = price
        self.__stock = 0

    def get_product_details(self) -> str:
        return f"Product ID: {self.__product_id}, Name: {self.__name}, Description: {self.__description}, Price: {self.__price}"

    def update_product_info(self, description=None, price=None):
        if description: self.__description = description
        if price is not None and price >= 0: self.__price = price

    def is_product_in_stock(self) -> bool:
        return self.__stock > 0

    def update_stock(self, quantity: int):
        if quantity >= 0:
            self.__stock = quantity


class OrderDetail:
    def __init__(self, detail_id: int, product: Product, quantity: int):
        self.__detail_id = detail_id
        self.__product = product
        self.__quantity = quantity
        self.__discount = 0.0

    def calculate_subtotal(self) -> float:
        return self.__product._Product__price * self.__quantity * (1 - self.__discount)

    def get_order_detail_info(self):
        return f"Order Detail ID: {self.__detail_id}, Product: {self.__product.get_product_details()}, Quantity: {self.__quantity}, Subtotal: {self.calculate_subtotal()}"

    def update_quantity(self, quantity: int):
        if quantity > 0:
            self.__quantity = quantity

    def add_discount(self, discount: float):
        if 0 <= discount <= 1:
            self.__discount = discount


class Order:
    def __init__(self, order_id: int, customer: Customer, date: datetime):
        self.__order_id = order_id
        self.__customer = customer
        self.__date = date
        self.__status = "Processing"
        self.__order_details = []

    def calculate_total_amount(self) -> float:
        return sum(detail.calculate_subtotal() for detail in self.__order_details)

    def get_order_details(self):
        details = [d.get_order_detail_info() for d in self.__order_details]
        return f"Order ID: {self.__order_id}, Status: {self.__status}, Date: {self.__date}, Details: {details}"

    def update_order_status(self, status: str):
        self.__status = status

    def cancel_order(self):
        self.__status = "Cancelled"

    def add_order_detail(self, detail: OrderDetail):
        self.__order_details.append(detail)


class Inventory:
    def __init__(self, inventory_id: int, product: Product, quantity: int, last_update: datetime):
        self.__inventory_id = inventory_id
        self.__product = product
        self.__quantity = quantity
        self.__last_update = last_update

    def add_to_inventory(self, quantity: int):
        if quantity > 0:
            self.__quantity += quantity
            self.__last_update = datetime.now()

    def remove_from_inventory(self, quantity: int):
        if 0 < quantity <= self.__quantity:
            self.__quantity -= quantity
            self.__last_update = datetime.now()


# Task 3: Object Instantiation and Usage
customer1 = Customer(1, "Lohitha", "Suggala", "lohitha@email.com", "1234567890", "Hyderabad")
product1 = Product(101, "Laptop", "Gaming Laptop", 100000.0)
product1.update_stock(10)
order1 = Order(5001, customer1, datetime.now())
detail1 = OrderDetail(1, product1, 2)
detail1.add_discount(0.1)
order1.add_order_detail(detail1)
customer1.add_order(order1)

# Task 4: Display Customer and Order Details
print(customer1.get_customer_details())
print(order1.get_order_details())

# Task 5: Product and Inventory Management
inventory1 = Inventory(1, product1, 10, datetime.now())
inventory1.add_to_inventory(5)
inventory1.remove_from_inventory(3)

# Task 6: Method Demonstrations
product1.update_product_info("Upgraded Gaming Laptop", 95000.0)
print(product1.get_product_details())

# Task 7: Use of Encapsulation and OOP Principles
# Already applied through getters/setters and class design

# Task 8: Handling User Input (can be expanded if needed)
def take_user_input():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    print(f"Thanks {name}, your email is {email}.")

# Uncomment to use:
# take_user_input()

# Task 9: Save Order and Customer Data to a File
with open("order_summary.txt", "w") as file:
    file.write(customer1.get_customer_details() + "\n")
    file.write(order1.get_order_details())