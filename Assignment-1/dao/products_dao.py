from util.db_conn_util import DBConnUtil
from entity.products import Product
from exception.user_defined_exception import ProductNotFoundException


class ProductDAO:
    def __init__(self):
        self.conn = DBConnUtil.get_connection()

    def get_product_details(self, product_id):
        cursor = self.conn.cursor()
        query = "SELECT * FROM Products WHERE ProductID = ?"
        cursor.execute(query, product_id)
        row = cursor.fetchone()

        if row:
            return Product(*row)
        else:
            raise ProductNotFoundException(f"No product found with ID {product_id}")

    def update_product_info(self, product_id, new_price, new_description):
        cursor = self.conn.cursor()
        query = """
            UPDATE Products
            SET Price = ?, Description = ?
            WHERE ProductID = ?
        """
        cursor.execute(query, new_price, new_description, product_id)
        self.conn.commit()
        print(f"✅ Product {product_id} updated successfully!")



