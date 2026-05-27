from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.projects_repository import ProjectsRepository
from api_messages.common_messages import message
from validators import validators

db = DatabaseConnectivity()
projects_repo = ProjectsRepository(db)


# ✅ CREATE PROJECT (Updated: Validates and injects product_id)
@app.route('/api/projects/create', methods=['POST'])
@jwt_required()
def create_project():
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)
        data = request.get_json()

        if not data.get('name'):
            return message.error({'error': 'name is required'}, 400)

        if not data.get('product_id'):
            return message.error({'error': 'product_id is required'}, 400)

        # Inject validated user contexts directly into dictionary
        data['user_id'] = user['id']

        project_id = projects_repo.create_project(data)

        return message.success({
            'id': project_id,
            'product_id': data['product_id'],
            'name': data['name']
        }, 201)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET ALL PROJECTS BY USER
@app.route('/api/projects', methods=['GET'])
@jwt_required()
def get_projects():
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        projects = projects_repo.get_projects_by_user(user['id'])
        return message.success(projects, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET ALL PROJECTS BY PRODUCT SCOPE (New Endpoint)
@app.route('/api/products/<int:product_id>/projects', methods=['GET'])
@jwt_required()
def get_projects_by_product(product_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        projects = projects_repo.get_projects_by_product(product_id)
        return message.success(projects, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET PROJECT BY ID
@app.route('/api/projects/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_by_id(project_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        project = projects_repo.get_project_by_id(project_id)

        if not project:
            return message.error({'error': 'Project not found'}, 404)

        return message.success(project, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ UPDATE PROJECT (Updated: Validates and updates product_id)
@app.route('/api/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json()

        if not data.get('name'):
            return message.error({'error': 'name is required'}, 400)

        if not data.get('product_id'):
            return message.error({'error': 'product_id is required'}, 400)

        existing_project = projects_repo.get_project_by_id(project_id)  # adjust method name to your repo
        if not existing_project:
            return message.error({'error': 'Project not found'}, 404)

        projects_repo.update_project(project_id, data)

        return message.success({
            'id': project_id,
            'product_id': data.get('product_id'),
            'name': data.get('name'),
            'status': data.get('status', 'ACTIVE')
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ DELETE PROJECT
@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        deleted = projects_repo.delete_project(project_id)

        if deleted == 0:
            return message.error({'error': 'Project not found'}, 404)

        return message.success({
            'message': 'Project deleted successfully',
            'id': project_id
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)