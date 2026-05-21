from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.team_members_repository import TeamMembersRepository
from api_messages.common_messages import message
from validators import validators

db = DatabaseConnectivity()

team_members_repo = TeamMembersRepository(db)


# ✅ ADD MEMBER TO TEAM
@app.route('/api/team-members/create', methods=['POST'])
@jwt_required()
def add_team_member():

    try:
        user_email = get_jwt_identity()

        user = validators.UserFlowValidator.validate_email(
            user_email
        )

        data = request.get_json()

        team_id = data.get('team_id')
        user_id = data.get('user_id')

        if not team_id:
            return message.error(
                {'error': 'team_id is required'},
                400
            )

        if not user_id:
            return message.error(
                {'error': 'user_id is required'},
                400
            )

        # ✅ CHECK DUPLICATE
        exists = team_members_repo.team_member_exists(
            team_id,
            user_id
        )

        if exists:
            return message.error(
                {'error': 'User already exists in this team'},
                409
            )

        member_id = team_members_repo.add_team_member(
            team_id,
            user_id
        )

        return message.success({
            'id': member_id,
            'team_id': team_id,
            'user_id': user_id
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


# ✅ REMOVE MEMBER FROM TEAM
@app.route('/api/team-members', methods=['DELETE'])
@jwt_required()
def remove_team_member():

    try:
        user_email = get_jwt_identity()

        user = validators.UserFlowValidator.validate_email(
            user_email
        )

        data = request.get_json()

        team_id = data.get('team_id')
        user_id = data.get('user_id')

        if not team_id:
            return message.error(
                {'error': 'team_id is required'},
                400
            )

        if not user_id:
            return message.error(
                {'error': 'user_id is required'},
                400
            )

        deleted = team_members_repo.remove_team_member(
            team_id,
            user_id
        )

        if deleted == 0:
            return message.error(
                {'error': 'Team member not found'},
                404
            )

        return message.success({
            'message': 'Member removed successfully',
            'team_id': team_id,
            'user_id': user_id
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
            'message': 'All team members removed',
            'deleted_count': deleted,
            'team_id': team_id
        }, 200)

    except Exception as e:

        return message.error(
            {'error': str(e)},
            500
        )