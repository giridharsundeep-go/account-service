from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.projects_individual_members_repository import ProjectIndividualMembersRepository
from api_messages.common_messages import message
from validators import validators

db = DatabaseConnectivity()
individual_members_repo = ProjectIndividualMembersRepository(db)


# ✅ SYNC / ASSIGN INDIVIDUAL MEMBERS TO PROJECT
@app.route('/api/project-individuals/sync', methods=['POST'])
@jwt_required()
def sync_project_individuals():
    try:
        # Extract and validate active user identity via JWT context
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json()
        project_id = data.get('project_id')
        user_account_ids = data.get('user_account_ids')  # Expects a list/array of IDs: [101, 102]

        if not project_id:
            return message.error({'error': 'project_id is required'}, 400)
        if user_account_ids is None or not isinstance(user_account_ids, list):
            return message.error({'error': 'user_account_ids must be a list'}, 400)

        # Triggers bulk sync, passing the current user['id'] as the tracking user_id
        individual_members_repo.assign_individuals_to_project(
            project_id=int(project_id),
            user_account_ids=user_account_ids,
            user_id=int(user['id'])
        )

        return message.success({
            'message': 'Project individual member allocations synchronized successfully',
            'project_id': project_id,
            'allocated_individuals_count': len(user_account_ids)
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET INDIVIDUAL MEMBERS BY PROJECT ID
@app.route('/api/project-individuals/<int:project_id>', methods=['GET'])
@jwt_required()
def get_individuals_by_project(project_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        # Pulls a flattened list of allocated user account IDs
        user_account_ids = individual_members_repo.get_individuals_by_project(project_id)
        return message.success(user_account_ids, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ REMOVE A SINGLE INDIVIDUAL MEMBER FROM A PROJECT
@app.route('/api/project-individuals/<int:project_id>/remove/<int:user_account_id>', methods=['DELETE'])
@jwt_required()
def remove_individual_from_project(project_id, user_account_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        deleted = individual_members_repo.remove_individual_from_project(project_id, user_account_id)

        if deleted == 0:
            return message.error({'error': 'Allocation mapping not found'}, 404)

        return message.success({
            'message': 'Individual specialist removed from project successfully',
            'project_id': project_id,
            'user_account_id': user_account_id
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)