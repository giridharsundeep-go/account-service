from database_connectivity import DatabaseConnectivity


class UsersRepository:

    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    # ✅ CREATE USER
    def create_user(
            self,
            user_id: int,
            role_id: int,
            name: str,
            email: str,
            is_active: bool,
            employee_id_prefix: str,
            employee_id_number: str,
            manager_id: int | None,
            location_country: str,
            location_state: str,
            location_city: str,
            location_work_model: str,
            location_desk_code: str
    ):
        query = """
            INSERT INTO users (
                user_id, role_id, name, email,
                is_active,
                employee_id_prefix, employee_id_number, manager_id,
                location_country, location_state, location_city, location_work_model, location_desk_code
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (
                user_id, role_id, name, email,
                int(is_active),  # Converted safely for tinyint columns
                employee_id_prefix, employee_id_number, manager_id,
                location_country, location_state, location_city, location_work_model, location_desk_code
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    # ✅ GET ALL USERS (New Master Fetch Method)
    def get_all_users(self):
        query = """
            SELECT 
                u.id,
                u.user_id,
                u.role_id,
                u.name,
                u.email,
                r.name AS role_name,

                -- Extended Matrix Attributes
                u.is_active,
                u.employee_id_prefix,
                u.employee_id_number,
                u.manager_id,
                m.name AS manager_name,

                u.location_country AS locationCountry,
                u.location_state AS locationState,
                u.location_city AS locationCity,
                u.location_work_model AS locationWorkModel,
                u.location_desk_code AS locationDeskCode,

                u.created_at
            FROM users u
            LEFT JOIN roles r
                ON u.role_id = r.id
            LEFT JOIN users m
                ON u.manager_id = m.id
            ORDER BY u.created_at DESC
        """

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query)
            return cursor.fetchall()
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

                -- Extended Matrix Attributes
                u.is_active,
                u.employee_id_prefix,
                u.employee_id_number,
                u.manager_id,
                m.name AS manager_name,

                u.location_country AS locationCountry,
                u.location_state AS locationState,
                u.location_city AS locationCity,
                u.location_work_model AS locationWorkModel,
                u.location_desk_code AS locationDeskCode,

                u.created_at
            FROM users u
            LEFT JOIN roles r
                ON u.role_id = r.id
            LEFT JOIN users m
                ON u.manager_id = m.id
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

                -- Extended Matrix Attributes
                u.is_active,
                u.employee_id_prefix,
                u.employee_id_number,
                u.manager_id,
                m.name AS manager_name,

                u.location_country AS locationCountry,
                u.location_state AS locationState,
                u.location_city AS locationCity,
                u.location_work_model AS locationWorkModel,
                u.location_desk_code AS locationDeskCode,

                u.created_at
            FROM users u
            LEFT JOIN roles r
                ON u.role_id = r.id
            LEFT JOIN users m
                ON u.manager_id = m.id
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
    def update_user(
            self,
            id: int,
            role_id: int,
            name: str,
            email: str,
            is_active: bool,
            employee_id_prefix: str,
            employee_id_number: str,
            manager_id: int | None,
            location_country: str,
            location_state: str,
            location_city: str,
            location_work_model: str,
            location_desk_code: str
    ):
        query = """
            UPDATE users
            SET role_id = %s,
                name = %s,
                email = %s,
                is_active = %s,
                employee_id_prefix = %s,
                employee_id_number = %s,
                manager_id = %s,
                location_country = %s,
                location_state = %s,
                location_city = %s,
                location_work_model = %s,
                location_desk_code = %s
            WHERE id = %s
        """

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (
                role_id, name, email,
                int(is_active),
                employee_id_prefix, employee_id_number, manager_id,
                location_country, location_state, location_city, location_work_model, location_desk_code,
                id
            ))
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