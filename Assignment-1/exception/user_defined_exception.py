class CustomerNotFoundException(Exception):
    def __init__(self, message="Customer not found."):
        super().__init__(message)

class ProductNotFoundException(Exception):
    def __init__(self, message="Product not found."):
        super().__init__(message)

class OrderNotFoundException(Exception):
    def __init__(self, message="Order not found."):
        super().__init__(message)

class InventoryNotFoundException(Exception):
    def __init__(self, message="Inventory item not found."):
        super().__init__(message)

