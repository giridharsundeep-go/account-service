from database_connectivity import DatabaseConnectivity


class OrganisationRepository:
    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    def create_organisation(self, data, user_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO organisations (title, description, email, phone, user_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.get('title'),
            data.get('description'),
            data.get('email'),
            data.get('phone'),
            user_id   # ✅ from JWT (NOT request)
        ))

        conn.commit()
        org_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return org_id

    def get_user_orgs(self, user_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, title, description, email, phone
            FROM organisations
            WHERE user_id = %s
        """, (user_id,))

        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result

    def get_org(self, id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
                   SELECT id, title, description, email, phone
                   FROM organisations
                   WHERE id = %s
               """, (id,))

        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result