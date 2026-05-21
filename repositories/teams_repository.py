from database_connectivity import DatabaseConnectivity


class TeamsRepository:

    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    # ✅ CREATE TEAM
    def create_team(self, user_id: int, name: str, description: str = None):

        query = """
            INSERT INTO teams (user_id, name, description)
            VALUES (%s, %s, %s)
        """

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                query,
                (user_id, name, description)
            )

            conn.commit()

            return cursor.lastrowid

        finally:
            cursor.close()
            conn.close()

    # ✅ GET ALL TEAMS BY USER
    def get_teams_by_user(self, user_id: int):

        query = """
            SELECT
                id,
                user_id,
                name,
                description,
                created_at
            FROM teams
            WHERE user_id = %s
            ORDER BY created_at DESC
        """

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (user_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    # ✅ GET TEAM BY ID
    def get_team_by_id(self, team_id: int):

        query = """
            SELECT
                id,
                user_id,
                name,
                description,
                created_at
            FROM teams
            WHERE id = %s
        """

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (team_id,))

            return cursor.fetchone()

        finally:
            cursor.close()
            conn.close()

    # ✅ UPDATE TEAM
    def update_team(
        self,
        team_id: int,
        name: str,
        description: str = None
    ):

        query = """
            UPDATE teams
            SET
                name = %s,
                description = %s
            WHERE id = %s
        """

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                query,
                (
                    name,
                    description,
                    team_id
                )
            )

            conn.commit()

            return cursor.rowcount

        finally:
            cursor.close()
            conn.close()

    # ✅ DELETE TEAM
    def delete_team(self, team_id: int):

        query = """
            DELETE FROM teams
            WHERE id = %s
        """

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (team_id,))

            conn.commit()

            return cursor.rowcount

        finally:
            cursor.close()
            conn.close()