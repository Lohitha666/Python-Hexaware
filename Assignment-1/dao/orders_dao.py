from exception.user_defined_exception import OrderNotFoundException
from util.db_conn_util import DBConnUtil

class OrderDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()

    def calculate_total_amount(self, order_id):
        cursor = self.conn.cursor()

        # Join OrderDetails and Products to get price and quantity
        query = """
            SELECT od.Quantity, p.Price
            FROM OrderDetails od
            JOIN Products p ON od.ProductID = p.ProductID
            WHERE od.OrderID = ?
        """
        cursor.execute(query, order_id)
        rows = cursor.fetchall()

        if not rows:
            raise OrderNotFoundException(f"No order found with ID {order_id}")

        total = sum(quantity * price for quantity, price in rows)
        return total

    def get_order_details(self, order_id):
        cursor = self.conn.cursor()
        query = """
            SELECT 
                od.OrderDetailID, 
                p.ProductName, 
                od.Quantity, 
                p.Price, 
                (od.Quantity * p.Price) AS Subtotal
            FROM OrderDetails od
            JOIN Products p ON od.ProductID = p.ProductID
            WHERE od.OrderID = ?
        """
        cursor.execute(query, (order_id,))
        rows = cursor.fetchall()

        if not rows:
            raise OrderNotFoundException(f"No details found for Order ID {order_id}")

        return rows


