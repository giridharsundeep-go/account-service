from database_connectivity import DatabaseConnectivity


class TeamMembersRepository:

    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    # ✅ ADD MEMBER TO TEAM
    def add_team_member(
        self,
        team_id: int,
        user_id: int
    ):

        query = """
            INSERT INTO team_members (
                team_id,
                user_id
            )
            VALUES (%s, %s)
        """

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                query,
                (
                    team_id,
                    user_id
                )
            )

            conn.commit()

            return cursor.lastrowid

        finally:
            cursor.close()
            conn.close()

    # ✅ GET MEMBERS BY TEAM
    def get_members_by_team(
        self,
        team_id: int
    ):

        query = """
            SELECT
                tm.id,
                tm.team_id,
                tm.user_id,
                u.name,
                u.email,
                u.role_id,
                r.name AS role_name
            FROM team_members tm

            INNER JOIN users u
                ON tm.user_id = u.id

            LEFT JOIN roles r
                ON u.role_id = r.id

            WHERE tm.team_id = %s

            ORDER BY u.name ASC
        """

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (team_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    # ✅ GET TEAMS BY USER
    def get_teams_by_user(
        self,
        user_id: int
    ):

        query = """
            SELECT
                tm.id,
                tm.team_id,
                t.name AS team_name,
                t.description,
                tm.user_id
            FROM team_members tm

            INNER JOIN teams t
                ON tm.team_id = t.id

            WHERE tm.user_id = %s

            ORDER BY t.name ASC
        """

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (user_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    # ✅ CHECK MEMBER EXISTS
    def team_member_exists(
        self,
        team_id: int,
        user_id: int
    ):

        query = """
            SELECT id
            FROM team_members
            WHERE team_id = %s
              AND user_id = %s
        """

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                query,
                (
                    team_id,
                    user_id
                )
            )

            return cursor.fetchone()

        finally:
            cursor.close()
            conn.close()

    # ✅ REMOVE MEMBER FROM TEAM
    def remove_team_member(
        self,
        team_id: int,
        user_id: int
    ):

        query = """
            DELETE FROM team_members
            WHERE team_id = %s
              AND user_id = %s
        """

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                query,
                (
                    team_id,
                    user_id
                )
            )

            conn.commit()

            return cursor.rowcount

        finally:
            cursor.close()
            conn.close()

    # ✅ REMOVE ALL MEMBERS FROM TEAM
    def remove_all_team_members(
        self,
        team_id: int
    ):

        query = """
            DELETE FROM team_members
            WHERE team_id = %s
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