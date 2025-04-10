from entity.products import Product
from util.db_conn_util import DBConnUtil
from exception.user_defined_exception import(InventoryNotFoundException,
                                             ProductNotFoundException)



class InventoryDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()

    def is_product_in_stock(self, product_id):
        cursor = self.conn.cursor()
        query = "SELECT QuantityInStock FROM Inventory WHERE ProductID = ?"
        cursor.execute(query, product_id)
        result = cursor.fetchone()

        if result and result[0] > 0:
            return True
        else:
            return False

    def get_product(self, product_id):
        cursor = self.conn.cursor()
        query = "SELECT * FROM Products WHERE ProductID = ?"
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()

        if row:
            return Product(*row)
        else:
            raise ProductNotFoundException(f"No product found with ID {product_id}")

    # Get the quantity in stock for a product
    def get_quantity_in_stock(self, product_id):
        cursor = self.conn.cursor()
        query = "SELECT QuantityInStock FROM Inventory WHERE ProductID = ?"
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()

        if row:
            return row[0]
        else:
            raise InventoryNotFoundException(f"No inventory record found for ProductID {product_id}")

    # Add a specified quantity to the inventory
    def add_to_inventory(self, product_id, quantity):
        cursor = self.conn.cursor()
        # Check if the inventory entry exists
        query_check = "SELECT QuantityInStock FROM Inventory WHERE ProductID = ?"
        cursor.execute(query_check, (product_id,))
        row = cursor.fetchone()

        if row:
            updated_quantity = row[0] + quantity
            update_query = "UPDATE Inventory SET QuantityInStock = ? WHERE ProductID = ?"
            cursor.execute(update_query, (updated_quantity, product_id))
        else:
            # If no record exists, insert new
            insert_query = "INSERT INTO Inventory (ProductID, QuantityInStock) VALUES (?, ?)"
            cursor.execute(insert_query, (product_id, quantity))

        self.conn.commit()
        print(f"✅ Inventory updated. Product {product_id} now has {quantity} more units.")

    def remove_from_inventory(self, product_id, quantity):
        cursor = self.conn.cursor()
        # First check current stock
        cursor.execute("SELECT QuantityInStock FROM Inventory WHERE ProductID = ?", (product_id,))
        row = cursor.fetchone()
        if not row:
            raise InventoryNotFoundException(f"No inventory found for product ID {product_id}")
        current_stock = row[0]

        if quantity > current_stock:
            raise Exception(f"Cannot remove {quantity} items. Only {current_stock} in stock.")

        new_stock = current_stock - quantity
        cursor.execute("UPDATE Inventory SET QuantityInStock = ? WHERE ProductID = ?", (new_stock, product_id))
        self.conn.commit()

    def update_stock_quantity(self, product_id, new_quantity):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Inventory WHERE ProductID = ?", (product_id,))
        if not cursor.fetchone():
            raise InventoryNotFoundException(f"No inventory found for product ID {product_id}")

        cursor.execute("UPDATE Inventory SET QuantityInStock = ? WHERE ProductID = ?", (new_quantity, product_id))
        self.conn.commit()

    def is_product_available(self, product_id, quantity_to_check):
        cursor = self.conn.cursor()
        cursor.execute("SELECT QuantityInStock FROM Inventory WHERE ProductID = ?", (product_id,))
        row = cursor.fetchone()
        if not row:
            raise InventoryNotFoundException(f"No inventory found for product ID {product_id}")

        current_stock = row[0]
        return current_stock >= quantity_to_check

    def get_inventory_value(self):
        cursor = self.conn.cursor()
        query = """
        SELECT I.ProductID, I.QuantityInStock, P.Price
        FROM Inventory I
        JOIN Products P ON I.ProductID = P.ProductID
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        total_value = sum(row[1] * row[2] for row in rows)
        return total_value

    def list_low_stock_products(self, threshold):
        cursor = self.conn.cursor()
        query = """
        SELECT P.ProductID, P.ProductName, I.QuantityInStock
        FROM Inventory I
        JOIN Products P ON I.ProductID = P.ProductID
        WHERE I.QuantityInStock < ?
        """
        cursor.execute(query, (threshold,))
        return cursor.fetchall()

    def list_out_of_stock_products(self):
        cursor = self.conn.cursor()
        query = """
        SELECT P.ProductID, P.ProductName
        FROM Inventory I
        JOIN Products P ON I.ProductID = P.ProductID
        WHERE I.QuantityInStock = 0
        """
        cursor.execute(query)
        return cursor.fetchall()

    def list_all_products(self):
        cursor = self.conn.cursor()
        query = """
            SELECT p.ProductID, p.ProductName, i.QuantityInStock
            FROM Products p
            JOIN Inventory i ON p.ProductID = i.ProductID
        """
        cursor.execute(query)
        return cursor.fetchall()