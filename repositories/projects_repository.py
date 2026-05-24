from database_connectivity import DatabaseConnectivity

class ProjectsRepository:
    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    # ✅ CREATE PROJECT (FIXED: Balanced column count and %s substitution markers to exactly 11)
    def create_project(self, data: dict):
        query = """
            INSERT INTO projects (
                user_id, name, description, methodology, priority, 
                total_backlog_points, sprint_duration_weeks, target_velocity, 
                auto_rollover_backlog, computed_sprint_count, computed_total_duration_weeks
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            params = (
                data['user_id'], data['name'], data.get('description'),
                data.get('methodology', 'AGILE_SCRUM'), data.get('priority', 'MEDIUM'),
                data.get('total_backlog_points', 0), data.get('sprint_duration_weeks'),
                data.get('target_velocity'), data.get('auto_rollover_backlog', 1),
                data.get('computed_sprint_count'), data.get('computed_total_duration_weeks')
            )
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    # ✅ GET ALL PROJECTS BY USER CONTEXT
    def get_projects_by_user(self, user_id: int):
        query = "SELECT * FROM projects WHERE user_id = %s ORDER BY created_at DESC"
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ✅ GET PROJECT BY ID
    def get_project_by_id(self, project_id: int):
        query = "SELECT * FROM projects WHERE id = %s"
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, (project_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    # ✅ UPDATE PROJECT
    def update_project(self, project_id: int, data: dict):
        query = """
            UPDATE projects
            SET name = %s, description = %s, methodology = %s, priority = %s,
                total_backlog_points = %s, sprint_duration_weeks = %s, 
                target_velocity = %s, auto_rollover_backlog = %s,
                computed_sprint_count = %s, computed_total_duration_weeks = %s
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            params = (
                data['name'], data.get('description'), data['methodology'], data['priority'],
                data.get('total_backlog_points'), data.get('sprint_duration_weeks'),
                data.get('target_velocity'), data.get('auto_rollover_backlog'),
                data.get('computed_sprint_count'), data.get('computed_total_duration_weeks'),
                project_id
            )
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ✅ DELETE PROJECT
    def delete_project(self, project_id: int):
        query = "DELETE FROM projects WHERE id = %s"
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, (project_id,))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()