from database_connectivity import DatabaseConnectivity

class StoriesRepository:
    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    # ✅ CREATE STORY
    def create_story(self, project_id: int, user_id: int, creator_user_id: int, title: str, description: str = None, epic_id: int = None, sprint_id: int = None, assignee_user_id: int = None, story_points: int = 0, status: str = 'BACKLOG', priority: str = 'MEDIUM'):
        query = """
            INSERT INTO stories (project_id, epic_id, sprint_id, user_id, creator_user_id, assignee_user_id, title, description, story_points, status, priority)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (project_id, epic_id, sprint_id, user_id, creator_user_id, assignee_user_id, title, description, story_points, status, priority))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    # ✅ GET STORIES BY PROJECT
    def get_stories_by_project(self, project_id: int):
        query = """
            SELECT id, project_id, epic_id, sprint_id, user_id, creator_user_id, assignee_user_id, title, description, story_points, status, priority, created_at, updated_at
            FROM stories
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

    # ✅ GET STORIES BY SPRINT (Crucial for your Sprint Lifecycle View & Auto-Rollover telemetry)
    def get_stories_by_sprint(self, sprint_id: int):
        query = """
            SELECT id, project_id, epic_id, sprint_id, user_id, creator_user_id, assignee_user_id, title, description, story_points, status, priority, created_at, updated_at
            FROM stories
            WHERE sprint_id = %s
            ORDER BY priority DESC, created_at ASC
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (sprint_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ✅ GET STORY BY ID
    def get_story_by_id(self, story_id: int):
        query = """
            SELECT id, project_id, epic_id, sprint_id, user_id, creator_user_id, assignee_user_id, title, description, story_points, status, priority, created_at, updated_at
            FROM stories
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (story_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    # ✅ UPDATE STORY
    def update_story(self, story_id: int, title: str, description: str, story_points: int, status: str, priority: str, epic_id: int = None, sprint_id: int = None, assignee_user_id: int = None):
        query = """
            UPDATE stories
            SET title = %s,
                description = %s,
                story_points = %s,
                status = %s,
                priority = %s,
                epic_id = %s,
                sprint_id = %s,
                assignee_user_id = %s
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (title, description, story_points, status, priority, epic_id, sprint_id, assignee_user_id, story_id))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ✅ DELETE STORY
    def delete_story(self, story_id: int):
        query = """
            DELETE FROM stories
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (story_id,))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()