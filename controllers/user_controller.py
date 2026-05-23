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

        # 🔧 Extract new organization and location metadata fields from payload
        is_active = data.get('is_active', True)
        employee_id_prefix = data.get('employee_id_prefix', '')
        employee_id_number = data.get('employee_id_number')  # Keep as None if missing/null
        manager_id = data.get('manager_id')  # Keep as None if missing/null

        # Mapping frontend camelCase keys to backend snake_case local variables
        location_country = data.get('locationCountry')
        location_state = data.get('locationState')
        location_city = data.get('locationCity')
        location_work_model = data.get('locationWorkModel', 'HQ')
        location_desk_code = data.get('locationDeskCode')

        # Pass all 13 fields sequentially to match your UsersRepository signatures
        user_id = users_repo.create_user(
            user['id'],
            role_id,
            name,
            email,
            is_active,
            employee_id_prefix,
            employee_id_number,
            manager_id,
            location_country,
            location_state,
            location_city,
            location_work_model,
            location_desk_code
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

        users = users_repo.get_all_users()

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

        # 🔧 Extract new fields for update operations as well
        is_active = data.get('is_active', True)
        employee_id_prefix = data.get('employee_id_prefix', '')
        employee_id_number = data.get('employee_id_number')
        manager_id = data.get('manager_id')

        location_country = data.get('locationCountry')
        location_state = data.get('locationState')
        location_city = data.get('locationCity')
        location_work_model = data.get('locationWorkModel', 'HQ')
        location_desk_code = data.get('locationDeskCode')

        # Ensure your users_repo.update_user signature accepts these extra positional arguments too!
        updated = users_repo.update_user(
            user_id,
            role_id,
            name,
            email,
            is_active,
            employee_id_prefix,
            employee_id_number,
            manager_id,
            location_country,
            location_state,
            location_city,
            location_work_model,
            location_desk_code
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