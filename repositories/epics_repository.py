from database_connectivity import DatabaseConnectivity

class EpicsRepository:
    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    # ✅ CREATE EPIC
    def create_epic(self, project_id: int, user_id: int, creator_user_id: int, epic_code: str, name: str, description: str, assignee_user_id: int, status: str = 'BACKLOG'):
        query = """
            INSERT INTO epics (project_id, user_id, creator_user_id, assignee_user_id, epic_code, name, description, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (project_id, user_id, creator_user_id, assignee_user_id, epic_code, name, description, status))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    # ✅ GET ALL EPICS BY PROJECT
    def get_epics_by_project(self, project_id: int):
        query = """
            SELECT id, project_id, user_id, creator_user_id, assignee_user_id, epic_code, name, description, status, created_at, updated_at
            FROM epics
            WHERE project_id = %s
            ORDER BY created_at DESC
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (project_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ✅ GET EPIC BY ID
    def get_epic_by_id(self, epic_id: int):
        query = """
            SELECT id, project_id, user_id, creator_user_id, assignee_user_id, epic_code, name, description, status, created_at, updated_at
            FROM epics
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (epic_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    # ✅ UPDATE EPIC
    def update_epic(self, epic_id: int, name: str, description: str, status: str, assignee_user_id: int = None):
        query = """
            UPDATE epics
            SET name = %s,
                description = %s,
                status = %s,
                assignee_user_id = %s
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (name, description, status, assignee_user_id, epic_id))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ✅ DELETE EPIC
    def delete_epic(self, epic_id: int):
        query = """
            DELETE FROM epics
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (epic_id,))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()