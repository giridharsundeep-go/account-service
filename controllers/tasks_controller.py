from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.tasks_repository import TasksRepository
from api_messages.common_messages import message
from validators import validators

db = DatabaseConnectivity()
tasks_repo = TasksRepository(db)


# ✅ CREATE TASK
@app.route('/api/tasks/create', methods=['POST'])
@jwt_required()
def create_task():
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)
        data = request.get_json()

        story_id = data.get('story_id')
        title = data.get('title')
        description = data.get('description')

        creator_user_id = data.get('creator_user_id', user['id'])
        assignee_user_id = data.get('assignee_user_id')
        status = data.get('status', 'TODO')

        if not story_id or not title:
            return message.error({'error': 'story_id and title are required fields'}, 400)

        task_id = tasks_repo.create_task(
            story_id=story_id,
            user_id=user['id'],
            creator_user_id=creator_user_id,
            assignee_user_id=assignee_user_id,
            title=title,
            description=description,
            status=status
        )

        return message.success({
            'id': task_id,
            'title': title,
            'status': status
        }, 201)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET TASKS BY STORY
@app.route('/api/stories/<int:story_id>/tasks', methods=['GET'])
@jwt_required()
def get_story_tasks(story_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        tasks = tasks_repo.get_tasks_by_story(story_id)
        return message.success(tasks, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET TASK BY ID
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        task = tasks_repo.get_task_by_id(task_id)
        if not task:
            return message.error({'error': 'Task not found'}, 404)

        return message.success(task, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ UPDATE TASK
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        status = data.get('status')
        assignee_user_id = data.get('assignee_user_id')

        if not title or not status:
            return message.error({'error': 'title and status are required fields'}, 400)

        updated = tasks_repo.update_task(
            task_id=task_id,
            title=title,
            description=description,
            status=status,
            assignee_user_id=assignee_user_id
        )

        if updated == 0:
            return message.error({'error': 'Task not found or no changes made'}, 404)

        return message.success({
            'id': task_id,
            'title': title,
            'status': status,
            'assignee_user_id': assignee_user_id
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        deleted = tasks_repo.delete_task(task_id)

        if deleted == 0:
            return message.error({'error': 'Task not found'}, 404)

        return message.success({
            'message': 'Task deleted successfully',
            'id': task_id
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)