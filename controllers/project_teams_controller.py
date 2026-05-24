from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.project_teams_repository import ProjectTeamsRepository
from api_messages.common_messages import message
from validators import validators

db = DatabaseConnectivity()
project_teams_repo = ProjectTeamsRepository(db)


# ✅ SYNC / ASSIGN TEAMS TO PROJECT
@app.route('/api/project-teams/sync', methods=['POST'])
@jwt_required()
def sync_project_teams():
    try:
        # Extract and validate active user identity via JWT context
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json()
        project_id = data.get('project_id')
        team_ids = data.get('team_ids')  # Expects a list/array of IDs: [1, 2, 3]

        if not project_id:
            return message.error({'error': 'project_id is required'}, 400)
        if team_ids is None or not isinstance(team_ids, list):
            return message.error({'error': 'team_ids must be a list'}, 400)

        # Triggers bulk sync, passing the required user_id for tracking allocations
        project_teams_repo.assign_teams_to_project(
            project_id=int(project_id),
            team_ids=team_ids,
            user_id=int(user['id'])
        )

        return message.success({
            'message': 'Project team allocations synchronized successfully',
            'project_id': project_id,
            'allocated_teams_count': len(team_ids)
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET TEAMS BY PROJECT ID
@app.route('/api/project-teams/<int:project_id>', methods=['GET'])
@jwt_required()
def get_teams_by_project(project_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        # Pulls a flattened list of allocated team IDs
        team_ids = project_teams_repo.get_teams_by_project(project_id)
        return message.success(team_ids, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ REMOVE A SINGLE TEAM FROM A PROJECT
@app.route('/api/project-teams/<int:project_id>/remove/<int:team_id>', methods=['DELETE'])
@jwt_required()
def remove_team_from_project(project_id, team_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        deleted = project_teams_repo.remove_team_from_project(project_id, team_id)

        if deleted == 0:
            return message.error({'error': 'Allocation mapping not found'}, 404)

        return message.success({
            'message': 'Team removed from project successfully',
            'project_id': project_id,
            'team_id': team_id
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)