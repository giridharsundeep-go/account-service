from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.users_repository import UsersRepository
from api_messages.common_messages import message
from validators import validators

db = DatabaseConnectivity()
users_repo = UsersRepository(db)


# ✅ CREATE USER
@app.route('/api/user/create', methods=['POST'])
@jwt_required()
def create_user():

    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        role_id = data.get('role_id')

        if not name:
            return message.error({'error': 'name is required'}, 400)

        if not email:
            return message.error({'error': 'email is required'}, 400)

        user_id = users_repo.create_user(
            user['id'],
            role_id,
            name,
            email
        )

        return message.success({
            'id': user_id,
            'name': name,
            'email': email,
            'role_id': role_id
        }, 201)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET USERS
@app.route('/api/user', methods=['GET'])
@jwt_required()
def get_users():

    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        users = users_repo.get_users_by_user(user['id'])

        return message.success(users, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ UPDATE USER
@app.route('/api/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):

    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        role_id = data.get('role_id')

        if not name:
            return message.error({'error': 'name is required'}, 400)

        if not email:
            return message.error({'error': 'email is required'}, 400)

        updated = users_repo.update_user(
            user_id,
            role_id,
            name,
            email
        )

        if updated == 0:
            return message.error({'error': 'User not found'}, 404)

        return message.success({
            'id': user_id,
            'name': name,
            'email': email,
            'role_id': role_id
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ DELETE USER
@app.route('/api/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):

    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        deleted = users_repo.delete_user(user_id)

        if deleted == 0:
            return message.error({'error': 'User not found'}, 404)

        return message.success({
            'message': 'User deleted successfully',
            'id': user_id
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)