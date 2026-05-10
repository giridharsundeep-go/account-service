

from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.org_repository import OrganisationRepository
from repositories.roles_repository import RolesRepository
from api_messages.common_messages import message
from repositories.user_account_repository import UserAccountRepository
from validators import validators

db = DatabaseConnectivity()
roles_repo = RolesRepository(db)
org_repo = OrganisationRepository(db)
user_repo = UserAccountRepository(db)

# ✅ CREATE ROLE
@app.route('/api/roles/create', methods=['POST'])
@jwt_required()
def create_org_role():
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)
        data = request.get_json()

        name = data.get('name')
        description = data.get('description')

        role_id = roles_repo.create_role(user['id'], name, description)

        return message.success({
            'id': role_id,
            'name': name
        }, 201)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET ROLES BY ORG
@app.route('/api/roles', methods=['GET'])
@jwt_required()
def get_roles():
    user_email = get_jwt_identity()
    user = validators.UserFlowValidator.validate_email(user_email)
    try:
        roles = roles_repo.get_roles_by_user(user['id'])
        return message.success(roles, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ UPDATE ROLE
@app.route('/api/roles/<int:role_id>', methods=['PUT'])
@jwt_required()
def update_role(role_id):
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json()

        name = data.get('name')
        description = data.get('description')

        if not name:
            return message.error({'error': 'name is required'}, 400)

        updated = roles_repo.update_role(role_id, name, description)

        if updated == 0:
            return message.error({'error': 'Role not found'}, 404)

        return message.success({
            'id': role_id,
            'name': name,
            'description': description
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ DELETE ROLE
@app.route('/api/roles/<int:role_id>', methods=['DELETE'])
@jwt_required()
def delete_role(role_id):
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        deleted = roles_repo.delete_role(role_id)

        if deleted == 0:
            return message.error({'error': 'Role not found'}, 404)

        return message.success({
            'message': 'Role deleted successfully',
            'id': role_id
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)