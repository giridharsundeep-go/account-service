from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.epics_repository import EpicsRepository
from api_messages.common_messages import message
from validators import validators

db = DatabaseConnectivity()
epics_repo = EpicsRepository(db)


# ✅ CREATE EPIC
@app.route('/api/epics/create', methods=['POST'])
@jwt_required()
def create_epic():
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)
        data = request.get_json()

        project_id = data.get('project_id')
        sprint_id = data.get('sprint_id')
        epic_code = data.get('epic_code')
        name = data.get('name')
        description = data.get('description')

        # Defaulting creator to the session user if not explicitly passed in payload
        creator_user_id = data.get('creator_user_id', user['id'])
        assignee_user_id = data.get('assignee_user_id')
        reporter_user_id = data.get('reporter_user_id')
        status = data.get('status', 'BACKLOG')

        if not project_id or not epic_code or not name:
            return message.error({'error': 'project_id, sprint_id, epic_code, and name are required fields'}, 400)

        epic_id = epics_repo.create_epic(
            project_id=project_id,
            sprint_id=sprint_id,
            user_id=user['id'],
            creator_user_id=creator_user_id,
            epic_code=epic_code,
            name=name,
            description=description,
            assignee_user_id=assignee_user_id,
            reporter_user_id=reporter_user_id,
            status=status
        )

        return message.success({
            'id': epic_id,
            'epic_code': epic_code,
            'name': name
        }, 201)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET ALL EPICS BY PROJECT ID
@app.route('/api/projects/<int:project_id>/epics', methods=['GET'])
@jwt_required()
def get_project_epics(project_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        epics = epics_repo.get_epics_by_project(project_id)
        return message.success(epics, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET EPIC BY ID
@app.route('/api/epics/<int:epic_id>', methods=['GET'])
@jwt_required()
def get_epic(epic_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        epic = epics_repo.get_epic_by_id(epic_id)
        if not epic:
            return message.error({'error': 'Epic not found'}, 404)

        return message.success(epic, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ UPDATE EPIC
@app.route('/api/epics/<int:epic_id>', methods=['PUT'])
@jwt_required()
def update_epic(epic_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        # 1. Check if epic exists first
        existing_epic = epics_repo.get_epic_by_id(epic_id)
        if not existing_epic:
            return message.error({'error': 'Epic not found'}, 404)

        data = request.get_json() or {}
        name = data.get('name')
        description = data.get('description')
        sprint_id = data.get('sprint_id')
        status = data.get('status')
        assignee_user_id = data.get('assignee_user_id')
        reporter_user_id = data.get('reporter_user_id')

        if not name or not status:
            return message.error({'error': 'name and status are required fields'}, 400)

        # 2. Perform update
        epics_repo.update_epic(
            epic_id=epic_id,
            name=name,
            description=description,
            sprint_id=sprint_id,
            status=status,
            assignee_user_id=assignee_user_id,
            reporter_user_id=reporter_user_id
        )

        return message.success({
            'id': epic_id,
            'name': name,
            'status': status,
            'assignee_user_id': assignee_user_id,
            'reporter_user_id': reporter_user_id
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)

# ✅ DELETE EPIC
@app.route('/api/epics/<int:epic_id>', methods=['DELETE'])
@jwt_required()
def delete_epic(epic_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        deleted = epics_repo.delete_epic(epic_id)

        if deleted == 0:
            return message.error({'error': 'Epic not found'}, 404)

        return message.success({
            'message': 'Epic deleted successfully',
            'id': epic_id
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)