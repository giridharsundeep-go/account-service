from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from controllers.sprints_controller import sprints_repo
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


@app.route('/api/projects/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_by_id(project_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        # 1. Fetch the base project details
        project = projects_repo.get_project_by_id(project_id)
        if not project:
            return message.error({'error': 'Project not found'}, 404)

        # Ensure project is a dictionary format we can mutate safely
        project_data = dict(project) if not isinstance(project, dict) else project.copy()

        # 2. Fetch all Sprints tied to this project
        # (Assuming sprints_repo has a get_sprints_by_project template)
        sprints = sprints_repo.get_sprints_by_project_id(project_id)
        project_data['sprints'] = [dict(s) for s in sprints] if sprints else []

        # 3. Fetch Teams and Individual User Info assigned to this project workspace
        # (Leverages a combined join query to get team structural layout + user identities)
        teams_and_users = projects_repo.get_project_teams_and_users(project_id)
        project_data['teams'] = teams_and_users if teams_and_users else []

        return message.success(project_data, 200)

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