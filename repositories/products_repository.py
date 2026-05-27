from database_connectivity import DatabaseConnectivity

class ProductsRepository:
    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    # ✅ CREATE PRODUCT
    def create_product(self, user_id: int, name: str, description: str = None):
        query = """
            INSERT INTO products (user_id, name, description)
            VALUES (%s, %s, %s)
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (user_id, name, description))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    # ✅ GET ALL PRODUCTS BY USER
    def get_products_by_user(self, user_id: int):
        query = """
            SELECT id, user_id, name, description, created_at
            FROM products
            WHERE user_id = %s
            ORDER BY created_at DESC
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ✅ GET PRODUCT BY ID
    def get_product_by_id(self, product_id: int):
        query = """
            SELECT id, user_id, name, description, created_at
            FROM products
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (product_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    # ✅ UPDATE PRODUCT
    def update_product(self, product_id: int, name: str, description: str = None):
        query = """
            UPDATE products
            SET name = %s,
                description = %s
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (name, description, product_id))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ✅ DELETE PRODUCT
    def delete_product(self, product_id: int):
        query = """
            DELETE FROM products
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (product_id,))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()