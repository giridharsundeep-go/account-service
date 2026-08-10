from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.sprints_repository import SprintsRepository
from api_messages.common_messages import message
from validators import validators


def get_sprints_repo():
    """Helper to instantiate repository with an active DB instance per request."""
    db = DatabaseConnectivity()
    return SprintsRepository(db)


# ✅ GET ALL SPRINTS (Optional Query Filter: ?project_id=1 or ?projectId=1)
@app.route('/api/sprints', methods=['GET'])
@jwt_required()
def get_sprints():
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        # Handle both snake_case and camelCase parameters safely
        project_id_raw = request.args.get('project_id') or request.args.get('projectId')
        project_id = int(project_id_raw) if project_id_raw and project_id_raw.isdigit() else None

        sprints_repo = get_sprints_repo()

        if project_id is not None:
            sprints = sprints_repo.get_sprints_by_project_id(project_id)
        else:
            sprints = sprints_repo.get_all_sprints()

        return message.success(sprints, 200)

    except Exception as e:
        app.logger.error(f"Error in GET /api/sprints: {str(e)}")
        return message.error({'error': str(e)}, 500)


# ✅ CREATE SPRINT
@app.route('/api/sprints/create', methods=['POST'])
@jwt_required()
def create_sprint():
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)
        data = request.get_json() or {}

        project_id = data.get('project_id') or data.get('projectId')
        name = data.get('name')
        goal = data.get('goal', '')
        start_date = data.get('start_date') or data.get('startDate')
        end_date = data.get('end_date') or data.get('endDate')
        status = data.get('status', 'PLANNED')

        if not project_id or not name:
            return message.error({'error': 'project_id and name are required fields'}, 400)

        sprints_repo = get_sprints_repo()
        sprint_id = sprints_repo.create_sprint(
            project_id=project_id,
            name=name,
            goal=goal,
            start_date=start_date,
            end_date=end_date,
            status=status,
            user_id=user['id'] if isinstance(user, dict) and 'id' in user else user
        )

        return message.success({
            'id': sprint_id,
            'projectId': project_id,
            'name': name,
            'goal': goal,
            'startDate': start_date,
            'endDate': end_date,
            'status': status
        }, 201)

    except Exception as e:
        app.logger.error(f"Error in POST /api/sprints/create: {str(e)}")
        return message.error({'error': str(e)}, 500)


# ✅ GET SPRINT BY ID
@app.route('/api/sprints/<int:sprint_id>', methods=['GET'])
@jwt_required()
def get_sprint_by_id(sprint_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        sprints_repo = get_sprints_repo()
        sprint = sprints_repo.get_sprint_by_id(sprint_id)
        if not sprint:
            return message.error({'error': 'Sprint not found'}, 404)

        return message.success(sprint, 200)

    except Exception as e:
        app.logger.error(f"Error in GET /api/sprints/{sprint_id}: {str(e)}")
        return message.error({'error': str(e)}, 500)


# ✅ UPDATE SPRINT
@app.route('/api/sprints/<int:sprint_id>', methods=['PUT'])
@jwt_required()
def update_sprint(sprint_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json() or {}
        name = data.get('name')
        goal = data.get('goal', '')
        start_date = data.get('start_date') or data.get('startDate')
        end_date = data.get('end_date') or data.get('endDate')
        status = data.get('status')
        is_current = data.get('is_current') if 'is_current' in data else data.get('isCurrent', False)

        if not name or not status:
            return message.error({'error': 'name and status are required fields'}, 400)

        sprints_repo = get_sprints_repo()
        updated = sprints_repo.update_sprint(
            sprint_id=sprint_id,
            name=name,
            goal=goal,
            start_date=start_date,
            end_date=end_date,
            status=status,
            is_current=is_current
        )

        if updated == 0:
            return message.error({'error': 'Sprint not found or no changes made'}, 404)

        return message.success({
            'id': sprint_id,
            'name': name,
            'status': status,
            'goal': goal,
            'startDate': start_date,
            'endDate': end_date,
            'isCurrent': is_current
        }, 200)

    except Exception as e:
        app.logger.error(f"Error in PUT /api/sprints/{sprint_id}: {str(e)}")
        return message.error({'error': str(e)}, 500)


# ✅ DELETE SPRINT
@app.route('/api/sprints/<int:sprint_id>', methods=['DELETE'])
@jwt_required()
def delete_sprint(sprint_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        sprints_repo = get_sprints_repo()
        deleted = sprints_repo.delete_sprint(sprint_id)

        if deleted == 0:
            return message.error({'error': 'Sprint not found'}, 404)

        return message.success({'message': 'Sprint deleted successfully', 'id': sprint_id}, 200)

    except Exception as e:
        app.logger.error(f"Error in DELETE /api/sprints/{sprint_id}: {str(e)}")
        return message.error({'error': str(e)}, 500)