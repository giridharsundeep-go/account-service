from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.teams_repository import TeamsRepository
from api_messages.common_messages import message
from validators import validators

db = DatabaseConnectivity()
teams_repo = TeamsRepository(db)


# ✅ CREATE TEAM
@app.route('/api/teams/create', methods=['POST'])
@jwt_required()
def create_team():

    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json()

        name = data.get('name')
        description = data.get('description')

        if not name:
            return message.error(
                {'error': 'name is required'},
                400
            )

        team_id = teams_repo.create_team(
            user['id'],
            name,
            description
        )

        return message.success({
            'id': team_id,
            'name': name,
            'description': description
        }, 201)

    except Exception as e:
        return message.error(
            {'error': str(e)},
            500
        )


# ✅ GET TEAMS
@app.route('/api/teams', methods=['GET'])
@jwt_required()
def get_teams():

    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        teams = teams_repo.get_teams_by_user(user['id'])

        return message.success(
            teams,
            200
        )

    except Exception as e:
        return message.error(
            {'error': str(e)},
            500
        )


# ✅ UPDATE TEAM
@app.route('/api/teams/<int:team_id>', methods=['PUT'])
@jwt_required()
def update_team(team_id):

    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json()

        name = data.get('name')
        description = data.get('description')

        if not name:
            return message.error(
                {'error': 'name is required'},
                400
            )

        updated = teams_repo.update_team(
            team_id,
            name,
            description
        )

        if updated == 0:
            return message.error(
                {'error': 'Team not found'},
                404
            )

        return message.success({
            'id': team_id,
            'name': name,
            'description': description
        }, 200)

    except Exception as e:
        return message.error(
            {'error': str(e)},
            500
        )


# ✅ DELETE TEAM
@app.route('/api/teams/<int:team_id>', methods=['DELETE'])
@jwt_required()
def delete_team(team_id):

    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        deleted = teams_repo.delete_team(team_id)

        if deleted == 0:
            return message.error(
                {'error': 'Team not found'},
                404
            )

        return message.success({
            'message': 'Team deleted successfully',
            'id': team_id
        }, 200)

    except Exception as e:
        return message.error(
            {'error': str(e)},
            500
        )