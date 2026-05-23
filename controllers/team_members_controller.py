from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.team_members_repository import TeamMembersRepository
from api_messages.common_messages import message
from validators import validators

db = DatabaseConnectivity()

team_members_repo = TeamMembersRepository(db)


# ✅ ADD MULTIPLE MEMBERS TO TEAM (BULK ENROLLMENT)
@app.route('/api/team-members/create', methods=['POST'])
@jwt_required()
def add_team_members():

    try:
        user_email = get_jwt_identity()

        user = validators.UserFlowValidator.validate_email(
            user_email
        )

        data = request.get_json()

        team_id = data.get('team_id')
        user_ids = data.get('user_ids')

        if not team_id:
            return message.error(
                {'error': 'team_id is required'},
                400
            )

        if not user_ids:
            return message.error(
                {'error': 'user_ids list is required'},
                400
            )

        if not isinstance(user_ids, list):
            return message.error(
                {'error': 'user_ids must be a valid array list'},
                400
            )

        # Bulk register execution utilizing our optimized repository method
        inserted_count = team_members_repo.add_team_members(
            team_id,
            user_ids
        )

        return message.success({
            'message': 'Team membership matrix processed successfully',
            'inserted_count': inserted_count,
            'team_id': team_id,
            'user_ids': user_ids
        }, 201)

    except Exception as e:

        return message.error(
            {'error': str(e)},
            500
        )


# ✅ GET MEMBERS BY TEAM
@app.route('/api/team-members/team/<int:team_id>', methods=['GET'])
@jwt_required()
def get_members_by_team(team_id):

    try:
        user_email = get_jwt_identity()

        user = validators.UserFlowValidator.validate_email(
            user_email
        )

        members = team_members_repo.get_members_by_team(
            team_id
        )

        return message.success(
            members,
            200
        )

    except Exception as e:

        return message.error(
            {'error': str(e)},
            500
        )


# ✅ GET TEAMS BY USER
@app.route('/api/team-members/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_teams_by_user(user_id):

    try:
        user_email = get_jwt_identity()

        user = validators.UserFlowValidator.validate_email(
            user_email
        )

        teams = team_members_repo.get_teams_by_user(
            user_id
        )

        return message.success(
            teams,
            200
        )

    except Exception as e:

        return message.error(
            {'error': str(e)},
            500
        )


# ✅ REMOVE MULTIPLE MEMBERS FROM TEAM (BULK PRUNING)
@app.route('/api/team-members', methods=['DELETE'])
@jwt_required()
def remove_team_members():

    try:
        user_email = get_jwt_identity()

        user = validators.UserFlowValidator.validate_email(
            user_email
        )

        data = request.get_json()

        team_id = data.get('team_id')
        user_ids = data.get('user_ids')

        if not team_id:
            return message.error(
                {'error': 'team_id is required'},
                400
            )

        if not user_ids:
            return message.error(
                {'error': 'user_ids list is required'},
                400
            )

        if not isinstance(user_ids, list):
            return message.error(
                {'error': 'user_ids must be a valid array list'},
                400
            )

        deleted = team_members_repo.remove_team_members(
            team_id,
            user_ids
        )

        if deleted == 0:
            return message.error(
                {'error': 'No matching team members found to remove'},
                404
            )

        return message.success({
            'message': 'Members removed successfully from the team target',
            'deleted_count': deleted,
            'team_id': team_id,
            'user_ids': user_ids
        }, 200)

    except Exception as e:

        return message.error(
            {'error': str(e)},
            500
        )


# ✅ REMOVE ALL MEMBERS FROM TEAM
@app.route('/api/team-members/team/<int:team_id>', methods=['DELETE'])
@jwt_required()
def remove_all_team_members(team_id):

    try:
        user_email = get_jwt_identity()

        user = validators.UserFlowValidator.validate_email(
            user_email
        )

        deleted = team_members_repo.remove_all_team_members(
            team_id
        )

        return message.success({
            'message': 'All team members removed successfully',
            'deleted_count': deleted,
            'team_id': team_id
        }, 200)

    except Exception as e:

        return message.error(
            {'error': str(e)},
            500
        )