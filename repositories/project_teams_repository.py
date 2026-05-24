class ProjectTeamsRepository:
    def __init__(self, db_connectivity):
        self.db = db_connectivity

    # ✅ FIXED: Added user_id parameter and mapped it to the SQL query & batch tuple
    def assign_teams_to_project(self, project_id: int, team_ids: list, user_id: int) -> bool:
        """
        Atomically drops historical team mappings for a project and rewrites
        them with the newly selected array of team IDs and tracking user_id.
        """
        if not project_id or not user_id:
            raise ValueError("project_id and user_id are required for resource sync operation")

        query_delete = "DELETE FROM project_teams WHERE project_id = %s"
        # Updated to include user_id column and the third positional %s placeholder
        query_insert = "INSERT INTO project_teams (project_id, team_id, user_id) VALUES (%s, %s, %s)"

        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Clear stale team maps
            cursor.execute(query_delete, (project_id,))

            # 2. Bulk insert new assignments if any are provided
            if team_ids:
                # FIXED: Balanced the parameters to match the 3-column SQL layout
                batch_payload = [(project_id, int(tid), user_id) for tid in team_ids]
                cursor.executemany(query_insert, batch_payload)

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_teams_by_project(self, project_id: int) -> list:
        """
        Retrieves all structural team IDs allocated to a specific initiative profile.
        """
        query = "SELECT team_id FROM project_teams WHERE project_id = %s"

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, (project_id,))
            records = cursor.fetchall()
            # Flatten dictionary nodes down into a raw integer array for Angular forms ingestion
            return [row['team_id'] for row in records]
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def remove_team_from_project(self, project_id: int, team_id: int) -> int:
        """
        Removes a single team allocation link out of an active project structure.
        """
        query = "DELETE FROM project_teams WHERE project_id = %s AND team_id = %s"

        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, (project_id, team_id))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()