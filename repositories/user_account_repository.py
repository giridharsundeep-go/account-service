from database_connectivity import DatabaseConnectivity


class UserAccountRepository:
    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    def get_user(self, email, phone):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM user_account WHERE email=%s OR phone=%s",
            (email, phone)
        )

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result

    def create_user(self, data, hashed):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO user_account 
            (first_name, last_name, email, phone, gender, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['firstName'],
            data['lastName'],
            data['email'],
            data['phone'],
            data['gender'],
            hashed
        ))

        conn.commit()

        cursor.close()
        conn.close()

    def get_user_by_email(self, email):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM user_account WHERE email=%s",
            (email,)
        )

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result