from database_connectivity import DatabaseConnectivity

class RolesRepository:
        def __init__(self, db: DatabaseConnectivity):
            self.db = db

        # ✅ CREATE ROLE
        def create_role(self, org_id: int, name: str, description: str = None):
            query = """
                INSERT INTO roles (user_id, name, description)
                VALUES (%s, %s, %s)
            """
            conn = self.db.get_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(query, (org_id, name, description))
                conn.commit()
                return cursor.lastrowid
            finally:
                cursor.close()
                conn.close()

        # ✅ GET ALL ROLES BY ORG
        def get_roles_by_user(self, org_id: int):
            query = """
                SELECT id, user_id, name, description, created_at
                FROM roles
                WHERE user_id = %s
                ORDER BY created_at DESC
            """
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)

            try:
                cursor.execute(query, (org_id,))
                return cursor.fetchall()
            finally:
                cursor.close()
                conn.close()

        # ✅ GET ROLE BY ID
        def get_role_by_id(self, role_id: int):
            query = """
                SELECT id, user_id, name, description, created_at
                FROM roles
                WHERE id = %s
            """
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)

            try:
                cursor.execute(query, (role_id,))
                return cursor.fetchone()
            finally:
                cursor.close()
                conn.close()

        # ✅ UPDATE ROLE
        def update_role(self, role_id: int, name: str, description: str = None):
            query = """
                UPDATE roles
                SET name = %s,
                    description = %s
                WHERE id = %s
            """
            conn = self.db.get_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(query, (name, description, role_id))
                conn.commit()
                return cursor.rowcount
            finally:
                cursor.close()
                conn.close()

        # ✅ DELETE ROLE
        def delete_role(self, role_id: int):
            query = """
                DELETE FROM roles
                WHERE id = %s
            """
            conn = self.db.get_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(query, (role_id,))
                conn.commit()
                return cursor.rowcount
            finally:
                cursor.close()
                conn.close()