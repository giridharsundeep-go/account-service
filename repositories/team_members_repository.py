from database_connectivity import DatabaseConnectivity


class TeamMembersRepository:

    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    # ✅ ADD MULTIPLE MEMBERS TO TEAM (BULK INSERT IN A SINGLE TRANSACTION)
    def add_team_members(
            self,
            team_id: int,
            user_ids: list[int]
    ):
        if not user_ids:
            return 0

        # IGNORE allows skipping duplicates safely if a user is already in the team
        query = """
            INSERT IGNORE INTO team_members (
                team_id, user_id
            )
            VALUES (%s, %s)
        """

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            # Prepare data tuples for executemany optimization
            payload_data = [(team_id, user_id) for user_id in user_ids]

            cursor.executemany(query, payload_data)
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ✅ GET MEMBERS BY TEAM (MATCHES USERSREPOSITORY ATTRIBUTE CASING)
    def get_members_by_team(self, team_id: int):
        query = """
            SELECT
                tm.id,
                tm.team_id,
                tm.user_id,
                u.user_id AS owner_user_id,
                u.role_id,
                u.name,
                u.email,
                r.name AS role_name,

                -- Extended Matrix Attributes matching frontend bindings
                u.is_active,
                u.employee_id_prefix,
                u.employee_id_number,
                u.manager_id,
                m.name AS manager_name,

                u.location_country AS locationCountry,
                u.location_state AS locationState,
                u.location_city AS locationCity,
                u.location_work_model AS locationWorkModel,
                u.location_desk_code AS locationDeskCode
            FROM team_members tm
            INNER JOIN users u
                ON tm.user_id = u.id
            LEFT JOIN roles r
                ON u.role_id = r.id
            LEFT JOIN users m
                ON u.manager_id = m.id
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
    def get_teams_by_user(self, user_id: int):
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
    def team_member_exists(self, team_id: int, user_id: int):
        query = """
            SELECT id
            FROM team_members
            WHERE team_id = %s
              AND user_id = %s
        """

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (team_id, user_id))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    # ✅ REMOVE SPECIFIC MEMBERS FROM TEAM (BULK DELETION SUPPORT)
    def remove_team_members(self, team_id: int, user_ids: list[int]):
        if not user_ids:
            return 0

        # Dynamically formats string based on list length to handle bulk deletions safely
        format_strings = ', '.join(['%s'] * len(user_ids))
        query = f"""
            DELETE FROM team_members
            WHERE team_id = %s
              AND user_id IN ({format_strings})
        """

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            # First argument is team_id, followed by all the user_id elements
            cursor.execute(query, [team_id] + user_ids)
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ✅ REMOVE ALL MEMBERS FROM TEAM
    def remove_all_team_members(self, team_id: int):
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