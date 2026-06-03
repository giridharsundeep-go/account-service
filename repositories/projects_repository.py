from database_connectivity import DatabaseConnectivity

class ProjectsRepository:
    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    # ✅ CREATE PROJECT (Fixed: Included project_code and balanced to 13 column markers)
    def create_project(self, data: dict):
        query = """
            INSERT INTO projects (
                user_id, product_id, project_code, name, description, methodology, priority, 
                total_backlog_points, sprint_duration_weeks, target_velocity, 
                auto_rollover_backlog, computed_sprint_count, computed_total_duration_weeks
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            params = (
                data['user_id'],
                data['product_id'],
                data.get('project_code', ''),  # Added project_code column parameter
                data['name'],
                data.get('description'),
                data.get('methodology', 'AGILE_SCRUM'),
                data.get('priority', 'MEDIUM'),
                data.get('total_backlog_points', 0),
                data.get('sprint_duration_weeks'),
                data.get('target_velocity'),
                data.get('auto_rollover_backlog', 1),
                data.get('computed_sprint_count'),
                data.get('computed_total_duration_weeks')
            )
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def get_project_teams_and_users(self, project_id):
        """
        Fetches all teams allocated to a project, along with a nested roster
        of individual user profiles belongs to those teams in one single sweep.
        """
        # 📝 Raw SQL Query matching your architectural entities
        query = """
            SELECT 
                t.id AS team_id,
                t.name AS team_name,
                t.department AS team_department,
                u.id AS user_id,
                u.first_name,
                u.last_name,
                u.email AS user_email,
                u.role AS user_role
            FROM project_teams pt
            INNER JOIN teams t ON pt.team_id = t.id
            LEFT JOIN team_members tm ON t.id = tm.team_id
            LEFT JOIN users u ON tm.user_id = u.id
            WHERE pt.project_id = :project_id
        """

        # Execute query using your existing database driver execute mechanism
        # e.g., db.execute(query, {'project_id': project_id})
        raw_rows = self.db.execute(query, {'project_id': project_id}).fetchall()

        # Process flat database rows into a structured object graph matrix
        teams_map = {}
        for row in raw_rows:
            tid = row['team_id']
            if tid not in teams_map:
                teams_map[tid] = {
                    'id': tid,
                    'name': row['team_name'],
                    'department': row['team_department'],
                    'members': []
                }

            # If an individual user exists inside this row slice, append them to the sub-roster
            if row['user_id']:
                teams_map[tid]['members'].append({
                    'id': row['user_id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['user_email'],
                    'role': row['user_role']
                })

        return list(teams_map.values())


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

    # ✅ GET ALL PROJECTS BY PRODUCT CONTEXT
    def get_projects_by_product(self, product_id: int):
        query = "SELECT * FROM projects WHERE product_id = %s ORDER BY created_at DESC"
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, (product_id,))
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

    # ✅ UPDATE PROJECT (Fixed: Included project_code updates safely)
    def update_project(self, project_id: int, data: dict):
        query = """
            UPDATE projects
            SET product_id = %s, 
                project_code = %s, 
                name = %s, 
                description = %s, 
                methodology = %s, 
                priority = %s,
                total_backlog_points = %s, 
                sprint_duration_weeks = %s, 
                target_velocity = %s, 
                auto_rollover_backlog = %s,
                computed_sprint_count = %s, 
                computed_total_duration_weeks = %s
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            params = (
                data['product_id'],
                data.get('project_code', ''),  # Added project_code mapping update tracking
                data['name'],
                data.get('description'),
                data['methodology'],
                data['priority'],
                data.get('total_backlog_points'),
                data.get('sprint_duration_weeks'),
                data.get('target_velocity'),
                data.get('auto_rollover_backlog'),
                data.get('computed_sprint_count'),
                data.get('computed_total_duration_weeks'),
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