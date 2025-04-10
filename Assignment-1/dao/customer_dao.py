from util.db_conn_util import DBConnUtil
from entity.customer import Customer
from exception.user_defined_exception import CustomerNotFoundException

class CustomerDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()

    def create_customer(self, customer):
        cursor = self.conn.cursor()
        query = """INSERT INTO Customers (CustomerID, FirstName, LastName, Email, Phone, Address)
                   VALUES (?, ?, ?, ?, ?, ?)"""
        cursor.execute(query, customer.customer_id, customer.first_name, customer.last_name,
                       customer.email, customer.phone, customer.address)
        self.conn.commit()
        print("Customer added successfully!")

    def read_customer(self, customer_id):
        cursor = self.conn.cursor()
        query = "SELECT * FROM Customers WHERE CustomerID = ?"
        cursor.execute(query, customer_id)
        row = cursor.fetchone()
        if row:
            return Customer(*row)
        else:
            raise CustomerNotFoundException(f"No customer found with ID {customer_id}")

    def update_customer(self, customer):
        cursor = self.conn.cursor()
        query = """UPDATE Customers
                   SET FirstName = ?, LastName = ?, Email = ?, Phone = ?, Address = ?
                   WHERE CustomerID = ?"""
        cursor.execute(query, customer.first_name, customer.last_name, customer.email,
                       customer.phone, customer.address, customer.customer_id)
        self.conn.commit()
        print("Customer updated successfully!")

    def delete_customer(self, customer_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM Customers WHERE CustomerID = ?"
        cursor.execute(query, customer_id)
        self.conn.commit()
        print("Customer deleted successfully!")

    def calculate_total_orders(self, customer_id):
        cursor = self.conn.cursor()
        query = "SELECT COUNT(*) FROM Orders WHERE CustomerID = ?"
        cursor.execute(query, customer_id)
        result = cursor.fetchone()
        total_orders = result[0] if result else 0
        return total_orders
