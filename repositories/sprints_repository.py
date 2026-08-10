import random
from database_connectivity import DatabaseConnectivity
from datetime import datetime


class SprintsRepository:
    def __init__(self, db: DatabaseConnectivity):
        self.db = db

    # ✅ GET ALL SPRINTS
    def get_all_sprints(self):
        query = """
            SELECT id, project_id, user_id, sprint_number, name, status, 
                   scheduled_start_date, scheduled_end_date, actual_start_at, 
                   actual_end_at, duration_weeks, target_velocity, activation_type,
                   created_at, updated_at
            FROM sprints
            ORDER BY id ASC
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ✅ GET SPRINTS BY PROJECT ID (Supports both alias names)
    def get_sprints_by_project_id(self, project_id: int):
        return self.get_sprints_by_project(project_id)

    def get_sprints_by_project(self, project_id: int):
        query = """
            SELECT id, project_id, user_id, sprint_number, name, status, 
                   scheduled_start_date, scheduled_end_date, actual_start_at, 
                   actual_end_at, duration_weeks, target_velocity, activation_type,
                   created_at, updated_at
            FROM sprints
            WHERE project_id = %s
            ORDER BY sprint_number ASC
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (project_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ✅ GET SPRINT BY ID
    def get_sprint_by_id(self, sprint_id: int):
        query = """
            SELECT id, project_id, user_id, sprint_number, name, status, 
                   scheduled_start_date, scheduled_end_date, actual_start_at, 
                   actual_end_at, duration_weeks, target_velocity, activation_type,
                   created_at, updated_at
            FROM sprints
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (sprint_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    # ✅ CREATE SINGLE SPRINT (Flexible signature supports both dict and kwargs)
    def create_sprint(self, sprint_data: dict = None, **kwargs):
        data = sprint_data if isinstance(sprint_data, dict) else kwargs

        query = """
            INSERT INTO sprints (
                project_id, user_id, sprint_number, name, status, 
                scheduled_start_date, scheduled_end_date, duration_weeks, 
                target_velocity, activation_type
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('project_id'),
            data.get('user_id'),
            data.get('sprint_number', 1),
            data.get('name'),
            data.get('status', 'PLANNED'),
            data.get('scheduled_start_date') or data.get('start_date'),
            data.get('scheduled_end_date') or data.get('end_date'),
            data.get('duration_weeks', 2),
            data.get('target_velocity', 0),
            data.get('activation_type', 'AUTOMATIC')
        )

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    # ✅ UPDATE SPRINT
    def update_sprint(self, sprint_id: int, **kwargs):
        name = kwargs.get('name')
        status = kwargs.get('status')
        start_date = kwargs.get('start_date') or kwargs.get('scheduled_start_date')
        end_date = kwargs.get('end_date') or kwargs.get('scheduled_end_date')

        query = """
            UPDATE sprints
            SET name = COALESCE(%s, name),
                status = COALESCE(%s, status),
                scheduled_start_date = COALESCE(%s, scheduled_start_date),
                scheduled_end_date = COALESCE(%s, scheduled_end_date),
                updated_at = %s
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (name, status, start_date, end_date, datetime.now(), sprint_id))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ✅ DELETE SPRINT
    def delete_sprint(self, sprint_id: int):
        query = "DELETE FROM sprints WHERE id = %s"
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (sprint_id,))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ✅ BULK INSERT CALIBRATED SPRINTS
    def bulk_insert_sprints(self, sprints_list: list):
        if not sprints_list:
            return False

        query = """
            INSERT INTO sprints (
                project_id, user_id, sprint_number, name, status, 
                scheduled_start_date, scheduled_end_date, duration_weeks, 
                target_velocity, activation_type
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        params = [
            (
                s['project_id'],
                s['user_id'],
                s['sprint_number'],
                s['name'],
                s.get('status', 'PLANNED'),
                s['scheduled_start_date'],
                s['scheduled_end_date'],
                s.get('duration_weeks', 2),
                s.get('target_velocity', 0),
                s.get('activation_type', 'AUTOMATIC')
            )
            for s in sprints_list
        ]

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.executemany(query, params)
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ✅ MANUALLY ACTIVATE A SPRINT
    def activate_sprint_manually(self, sprint_id: int):
        query = """
            UPDATE sprints
            SET status = 'ACTIVE',
                actual_start_at = %s
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (datetime.now(), sprint_id))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ✅ MANUALLY COMPLETE A SPRINT
    def complete_sprint_manually(self, sprint_id: int):
        query = """
            UPDATE sprints
            SET status = 'COMPLETED',
                actual_end_at = %s
            WHERE id = %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (datetime.now(), sprint_id))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ✅ GET PLANNED AUTOMATED SPRINTS BY DATE
    def get_automatic_sprints_to_activate(self, check_date: str):
        query = """
            SELECT id, project_id, user_id, sprint_number, name
            FROM sprints
            WHERE status = 'PLANNED' 
              AND activation_type = 'AUTOMATIC' 
              AND scheduled_start_date <= %s
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (check_date,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # 🔄 ATOMIC SYNC & UPSERT ROUTINE
    def sync_and_recreate_planned_sprints(self, project_id: int, sprints_list: list):
        if not sprints_list:
            return 0

        query = """
            INSERT INTO sprints (
                project_id, user_id, sprint_number, name, status, 
                scheduled_start_date, scheduled_end_date, duration_weeks, 
                target_velocity, activation_type
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                user_id = VALUES(user_id),
                scheduled_start_date = VALUES(scheduled_start_date),
                scheduled_end_date = VALUES(scheduled_end_date),
                duration_weeks = VALUES(duration_weeks),
                target_velocity = VALUES(target_velocity),
                activation_type = VALUES(activation_type)
        """

        params = [
            (
                project_id,
                int(s['user_id']),
                int(s['sprint_number']),
                s['name'],
                s.get('status', 'PLANNED'),
                s['scheduled_start_date'],
                s['scheduled_end_date'],
                int(s.get('duration_weeks', 2)),
                int(s.get('target_velocity', 0)),
                s.get('activation_type', 'AUTOMATIC')
            )
            for s in sprints_list
        ]

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.executemany(query, params)

            processed_sprint_numbers = [int(s['sprint_number']) for s in sprints_list]
            format_strings = ','.join(['%s'] * len(processed_sprint_numbers))

            delete_query = f"""
                DELETE FROM sprints 
                WHERE project_id = %s 
                  AND sprint_number NOT IN ({format_strings}) 
                  AND status = 'PLANNED'
            """
            cursor.execute(delete_query, [project_id] + processed_sprint_numbers)

            conn.commit()
            return len(sprints_list)

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()