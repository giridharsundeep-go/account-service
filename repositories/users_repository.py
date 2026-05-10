from database_connectivity import DatabaseConnectivity


class UsersRepository:

    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    # ✅ CREATE USER
    def create_user(self, user_id: int, name: str, email: str):
        query = """
            INSERT INTO users (user_id, name, email)
            VALUES (%s, %s, %s)
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (user_id, name, email))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    # ✅ GET USERS BY USER (owner)
    def get_users_by_user(self, user_id: int):
        query = """
            SELECT id, user_id, name, email, created_at
            FROM users
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

    # ✅ GET USER BY ID
    def get_user_by_id(self, id: int):
        query = """
            SELECT id, user_id, name, email, created_at
            FROM users
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    # ✅ UPDATE USER
    def update_user(self, id: int, name: str, email: str):
        query = """
            UPDATE users
            SET name = %s,
                email = %s
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (name, email, id))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ✅ DELETE USER
    def delete_user(self, id: int):
        query = """
            DELETE FROM users
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()