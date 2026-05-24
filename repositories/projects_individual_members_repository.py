class ProjectIndividualMembersRepository:
    def __init__(self, db_connectivity):
        self.db = db_connectivity

    def assign_individuals_to_project(self, project_id: int, user_account_ids: list, user_id: int) -> bool:
        """
        Atomically drops historical individual member mappings for a project and rewrites
        them with the newly selected array of user account IDs and the tracking user_id.
        """
        if not project_id or not user_id:
            raise ValueError("project_id and user_id are required for individual resource sync operation")

        query_delete = "DELETE FROM project_individual_members WHERE project_id = %s"
        query_insert = """
            INSERT INTO project_individual_members (project_id, user_account_id, user_id) 
            VALUES (%s, %s, %s)
        """

        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Clear out historic individual user assignments for this project
            cursor.execute(query_delete, (project_id,))

            # 2. Bulk insert fresh individual assignments if provided
            if user_account_ids:
                # Balanced tuple matching: project_id, assigned target user, creator tracking user_id
                batch_payload = [(project_id, int(uaid), user_id) for uaid in user_account_ids]
                cursor.executemany(query_insert, batch_payload)

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_individuals_by_project(self, project_id: int) -> list:
        """
        Retrieves all independent user account IDs allocated to a specific project.
        """
        query = "SELECT user_account_id FROM project_individual_members WHERE project_id = %s"

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, (project_id,))
            records = cursor.fetchall()
            # Flatten into an array of integers for clean Angular form bindings
            return [row['user_account_id'] for row in records]
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def remove_individual_from_project(self, project_id: int, user_account_id: int) -> int:
        """
        Removes a single independent contractor/specialist mapping out of an active project structure.
        """
        query = "DELETE FROM project_individual_members WHERE project_id = %s AND user_account_id = %s"

        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, (project_id, user_account_id))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()