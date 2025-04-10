from util.db_conn_util import DBConnUtil
from decimal import Decimal


class Order_Details_DAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()

    def calculate_subtotal(self, order_id, product_id):
        cursor = self.conn.cursor()
        query = """
            SELECT od.Quantity, p.Price
            FROM OrderDetails od
            JOIN Products p ON od.ProductID = p.ProductID
            WHERE od.OrderID = ? AND od.ProductID = ?
        """
        cursor.execute(query, (order_id, product_id))
        row = cursor.fetchone()

        if row:
            quantity, price = row
            return quantity * price
        else:
            raise Exception(f"No order detail found for OrderID {order_id} and ProductID {product_id}")

    def get_order_detail_info(self, order_detail_id):
        cursor = self.conn.cursor()
        query = """
            SELECT od.OrderDetailID, od.OrderID, od.ProductID, od.Quantity, p.ProductName, p.Price
            FROM OrderDetails od
            JOIN Products p ON od.ProductID = p.ProductID
            WHERE od.OrderDetailID = ?
        """
        cursor.execute(query, (order_detail_id,))
        row = cursor.fetchone()

        if row:
            return {
                "OrderDetailID": row[0],
                "OrderID": row[1],
                "ProductID": row[2],
                "Quantity": row[3],
                "ProductName": row[4],
                "Price": row[5],
                "Subtotal": row[3] * row[5]
            }
        else:
            raise Exception(f"No order detail found with ID {order_detail_id}")



    def update_quantity(self, order_detail_id, new_quantity):
        cursor = self.conn.cursor()
        query = "UPDATE OrderDetails SET Quantity = ? WHERE OrderDetailID = ?"
        cursor.execute(query, (new_quantity, order_detail_id))
        self.conn.commit()
        print(f"✅ Quantity updated for OrderDetailID {order_detail_id}.")



    def add_discount(self, order_detail_id, discount_percent):
        cursor = self.conn.cursor()

        query = """
            SELECT od.Quantity, p.Price
            FROM OrderDetails od
            JOIN Products p ON od.ProductID = p.ProductID
            WHERE od.OrderDetailID = ?
        """
        cursor.execute(query, (order_detail_id,))
        row = cursor.fetchone()

        if not row:
            raise Exception(f"OrderDetail ID {order_detail_id} not found.")

        quantity, price = row
        quantity = int(quantity)
        price = Decimal(price)  # Ensure it's a Decimal
        discount_decimal = Decimal(str(discount_percent)) / Decimal("100")

        subtotal = price * quantity
        discount_amount = subtotal * discount_decimal
        final_total = subtotal - discount_amount

        return {
            "Original Subtotal": subtotal,
            "Discount": discount_amount,
            "Final Total": final_total
        }