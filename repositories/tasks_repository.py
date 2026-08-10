from database_connectivity import DatabaseConnectivity

class TasksRepository:
    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    # ✅ GET ALL TASKS (with optional sprint filtering)
    def get_tasks(self, sprint_id: int = None):
        query = """
            SELECT id, story_id, sprint_id, user_id, creator_user_id, assignee_user_id, reporter_user_id, title, description, status, created_at, updated_at
            FROM tasks
            """
        params = []
        if sprint_id is not None:
            query += " WHERE sprint_id = %s"
            params.append(sprint_id)

        query += " ORDER BY created_at ASC"

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, tuple(params) if params else ())
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

        # ✅ CREATE TASK
    def create_task(self, story_id: int, sprint_id: int, user_id: int, creator_user_id: int, title: str,
                        description: str = None, assignee_user_id: int = None, reporter_user_id: int = None,
                        status: str = 'TODO'):
        query = """
                INSERT INTO tasks (story_id, sprint_id, user_id, creator_user_id, assignee_user_id, reporter_user_id, title, description, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query,
                               (story_id, sprint_id, user_id, creator_user_id, assignee_user_id, reporter_user_id,
                                title, description, status))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    # ✅ GET TASKS BY STORY
    def get_tasks_by_story(self, story_id: int):
        query = """
            SELECT id, story_id, sprint_id, user_id, creator_user_id, assignee_user_id, reporter_user_id, title, description, status, created_at, updated_at
            FROM tasks
            WHERE story_id = %s
            ORDER BY created_at ASC
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (story_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ✅ GET TASK BY ID
    def get_task_by_id(self, task_id: int):
        query = """
            SELECT id, story_id, sprint_id, user_id, creator_user_id, assignee_user_id, reporter_user_id, title, description, status, created_at, updated_at
            FROM tasks
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (task_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    # ✅ UPDATE TASK
    def update_task(self, task_id: int, title: str, description: str, sprint_id: int, status: str, assignee_user_id: int = None, reporter_user_id: int = None):
        query = """
            UPDATE tasks
            SET title = %s,
                description = %s,
                sprint_id = %s,
                status = %s,
                assignee_user_id = %s,
                reporter_user_id = %s
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (title, description, sprint_id, status, assignee_user_id, reporter_user_id, task_id))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ✅ DELETE TASK
    def delete_task(self, task_id: int):
        query = """
            DELETE FROM tasks
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (task_id,))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()