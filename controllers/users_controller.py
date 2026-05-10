from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from api_messages.common_messages import message
from repositories.user_account_repository import UserAccountRepository
from validators import validators

db = DatabaseConnectivity()
user_repo = UserAccountRepository(db)


# ✅ CREATE USER
@app.route('/api/users/create', methods=['POST'])
@jwt_required()
def create_user():
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json()

        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return message.error({'error': 'name and email are required'}, 400)

        user_id = user_repo.create_user(
            user_id=user['id'],     # from JWT (user_account)
            org_id=user['org_id'], # assuming validator returns this
            name=name,
            email=email
        )

        return message.success({
            'id': user_id,
            'name': name,
            'email': email
        }, 201)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET USERS BY ORG
@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        users = user_repo.get_users_by_org(user['org_id'])

        return message.success(users, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ UPDATE USER
@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json()

        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return message.error({'error': 'name and email are required'}, 400)

        updated = user_repo.update_user(user_id, name, email)

        if updated == 0:
            return message.error({'error': 'User not found'}, 404)

        return message.success({
            'id': user_id,
            'name': name,
            'email': email
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ DELETE USER
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        deleted = user_repo.delete_user(user_id)

        if deleted == 0:
            return message.error({'error': 'User not found'}, 404)

        return message.success({
            'message': 'User deleted successfully',
            'id': user_id
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)