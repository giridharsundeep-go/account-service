from database_connectivity import DatabaseConnectivity


class UsersRepository:

    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    # ✅ CREATE USER
    def create_user(self, user_id: int, role_id: int, name: str, email: str):
        query = """
            INSERT INTO users (user_id, role_id, name, email)
            VALUES (%s, %s, %s, %s)
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (user_id, role_id, name, email))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    # ✅ GET USERS BY OWNER USER
    def get_users_by_user(self, user_id: int):
        query = """
            SELECT 
                u.id,
                u.user_id,
                u.role_id,
                u.name,
                u.email,
                r.name AS role_name,
                u.created_at
            FROM users u
            LEFT JOIN roles r
                ON u.role_id = r.id
            WHERE u.user_id = %s
            ORDER BY u.created_at DESC
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
            SELECT 
                u.id,
                u.user_id,
                u.role_id,
                u.name,
                u.email,
                r.name AS role_name,
                u.created_at
            FROM users u
            LEFT JOIN roles r
                ON u.role_id = r.id
            WHERE u.id = %s
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
    def update_user(self, id: int, role_id: int, name: str, email: str):
        query = """
            UPDATE users
            SET role_id = %s,
                name = %s,
                email = %s
            WHERE id = %s
        """

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (role_id, name, email, id))
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