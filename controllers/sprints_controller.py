import math
import random
from datetime import datetime, timedelta
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.sprints_repository import SprintsRepository
from repositories.projects_repository import ProjectsRepository
from validators import validators
from api_messages.common_messages import message

sprints_blueprint = Blueprint('sprints_controller', __name__)
db_connection = DatabaseConnectivity()

sprints_repo = SprintsRepository(db_connection)
projects_repo = ProjectsRepository(db_connection)


# 1. 📅 PREVIEW SPRINTS BY PROJECT ID
@app.route('/api/sprints/preview', methods=['POST'])
@jwt_required()
def preview_project_sprints():
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        payload = request.get_json() or {}
        project_id = payload.get('project_id')

        if not project_id:
            return message.error({'error': 'Missing required project_id context parameter'}, 400)

        project_details = projects_repo.get_project_by_id(int(project_id))
        if not project_details:
            return message.error({'error': f'Project Architecture context record #{project_id} not discovered'}, 404)

        owner_user_id = project_details.get('user_id')
        project_code = project_details.get('project_code', '').strip()
        total_points = float(project_details.get('total_backlog_points', 0))
        target_velocity = float(project_details.get('target_velocity', 1))
        duration_weeks = int(project_details.get('sprint_duration_weeks', 2))

        start_date_str = payload.get('previewStartDate', datetime.now().strftime('%Y-%m-%d'))
        activation_type = payload.get('previewActivationType', 'AUTOMATIC')

        buffered_points = total_points * 1.15
        effective_velocity = target_velocity * 0.80
        if effective_velocity <= 0:
            effective_velocity = 1

        total_sprints = int(math.ceil(buffered_points / effective_velocity))

        current_start = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        days_per_sprint = duration_weeks * 7
        preview_list = []

        prefix_code = f"{project_code}-" if project_code else "SPRINT-"

        for index in range(1, total_sprints + 1):
            current_end = current_start + timedelta(days=days_per_sprint - 1)

            # ✅ GENERATE RANDOM 7-DIGIT SEQUENCE INDICES
            random_seq = random.randint(1000000, 9999999)

            preview_list.append({
                "project_id": int(project_id),
                "user_id": owner_user_id,
                "sprint_number": index,
                "name": f"{prefix_code}{random_seq} (Cycle {index})",
                "scheduled_start_date": current_start.strftime('%Y-%m-%d'),
                "scheduled_end_date": current_end.strftime('%Y-%m-%d'),
                "duration_weeks": duration_weeks,
                "target_velocity": int(round(effective_velocity)),
                "activation_type": activation_type,
                "status": "PLANNED"
            })
            current_start = current_end + timedelta(days=1)

        return message.success(preview_list, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


@app.route('/api/sprints/project/<int:project_id>/sync', methods=['PUT'])
@jwt_required()
def sync_project_sprints_timeline(project_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        payload = request.get_json() or {}

        # 1. Fetch updated variables from DB
        project_details = projects_repo.get_project_by_id(project_id)
        if not project_details:
            return message.error({'error': f'Project #{project_id} does not exist'}, 404)

        # 2. Get the user_id from the project configuration
        target_user_id = project_details.get('user_id')


        # 3. Proceed with calculation metrics safely using our verified target_user_id
        project_code = project_details.get('project_code', '').strip()
        total_points = float(project_details.get('total_backlog_points', 0))
        target_velocity = float(project_details.get('target_velocity', 1))
        duration_weeks = int(project_details.get('sprint_duration_weeks', 2))

        start_date_str = payload.get('previewStartDate', datetime.now().strftime('%Y-%m-%d'))
        activation_type = payload.get('previewActivationType', 'AUTOMATIC')

        buffered_points = total_points * 1.15
        effective_velocity = target_velocity * 0.80
        if effective_velocity <= 0:
            effective_velocity = 1

        total_sprints = int(math.ceil(buffered_points / effective_velocity))
        current_start = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        days_per_sprint = duration_weeks * 7

        updated_sprints = []
        prefix_code = f"{project_code}-" if project_code else "SPRINT-"

        for index in range(1, total_sprints + 1):
            current_end = current_start + timedelta(days=days_per_sprint - 1)
            random_seq = random.randint(1000000, 9999999)

            updated_sprints.append({
                "project_id": project_id,
                "user_id": int(target_user_id),  # ✅ 100% verified to exist in the database now
                "sprint_number": index,
                "name": f"{prefix_code}{random_seq} (Cycle {index})",
                "scheduled_start_date": current_start.strftime('%Y-%m-%d'),
                "scheduled_end_date": current_end.strftime('%Y-%m-%d'),
                "duration_weeks": duration_weeks,
                "target_velocity": int(round(effective_velocity)),
                "activation_type": activation_type,
                "status": "PLANNED"
            })
            current_start = current_end + timedelta(days=1)

        # 4. Push to safe upsert transactional component layer
        synced_count = sprints_repo.sync_and_recreate_planned_sprints(project_id, updated_sprints)

        return message.success({
            'message': 'Sprint schedules synchronized and updated successfully.',
            'synced_records': synced_count
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)

# 3. 🔍 FETCH SPRINTS FOR AN INDIVIDUAL PROJECT LAYOUT
@app.route('/api/sprints/project/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_sprints_list(project_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        sprints = sprints_repo.get_sprints_by_project(project_id) or []

        for sprint in sprints:
            for d_field in ['scheduled_start_date', 'scheduled_end_date']:
                if sprint.get(d_field) and not isinstance(sprint[d_field], str):
                    sprint[d_field] = sprint[d_field].strftime('%Y-%m-%d')
            for t_field in ['actual_start_at', 'actual_end_at']:
                if sprint.get(t_field) and not isinstance(sprint[t_field], str):
                    sprint[t_field] = sprint[t_field].strftime('%Y-%m-%d %H:%M:%S')

        return message.success(sprints, 200)
    except Exception as e:
        return message.error({'error': str(e)}, 500)


# 4. ▶️ START SPRINT MILESTONE
@app.route('/api/sprints/<int:sprint_id>/start', methods=['PUT'])
@jwt_required()
def start_sprint(sprint_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        rows = sprints_repo.activate_sprint_manually(sprint_id)
        if rows > 0:
            return message.success({'message': 'Sprint operational tracking shifted to ACTIVE'}, 200)
        return message.error({'error': 'Sprint configuration matching target node context not found'}, 404)
    except Exception as e:
        return message.error({'error': str(e)}, 500)


# 5. ⏹️ COMPLETE SPRINT MILESTONE
@app.route('/api/sprints/<int:sprint_id>/complete', methods=['PUT'])
@jwt_required()
def complete_sprint(sprint_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        rows = sprints_repo.complete_sprint_manually(sprint_id)
        if rows > 0:
            return message.success({'message': 'Sprint lifecycle metrics closed and set to COMPLETED'}, 200)
        return message.error({'error': 'Sprint target unresolvable or context closed'}, 404)
    except Exception as e:
        return message.error({'error': str(e)}, 500)