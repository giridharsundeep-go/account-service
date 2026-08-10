from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.stories_repository import StoriesRepository
from api_messages.common_messages import message
from validators import validators

db = DatabaseConnectivity()
stories_repo = StoriesRepository(db)


# ✅ CREATE STORY
@app.route('/api/stories/create', methods=['POST'])
@jwt_required()
def create_story():
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)
        data = request.get_json()

        project_id = data.get('project_id')
        title = data.get('title')
        description = data.get('description')
        epic_id = data.get('epic_id')
        sprint_id = data.get('sprint_id') or data.get('sprintId')

        creator_user_id = data.get('creator_user_id', user['id'])
        assignee_user_id = data.get('assignee_user_id')
        reporter_user_id = data.get('reporter_user_id')
        story_points = data.get('story_points', 0)
        status = data.get('status', 'BACKLOG')
        priority = data.get('priority', 'MEDIUM')

        if not project_id or not title:
            return message.error({'error': 'project_id and title are required fields'}, 400)

        story_id = stories_repo.create_story(
            project_id=project_id,
            user_id=user['id'],
            creator_user_id=creator_user_id,
            assignee_user_id=assignee_user_id,
            reporter_user_id=reporter_user_id,
            epic_id=epic_id,
            sprint_id=sprint_id,
            title=title,
            description=description,
            story_points=story_points,
            status=status,
            priority=priority
        )

        return message.success({
            'id': story_id,
            'title': title,
            'status': status,
            'sprint_id': sprint_id
        }, 201)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET STORIES BY PROJECT
@app.route('/api/projects/<int:project_id>/stories', methods=['GET'])
@jwt_required()
def get_project_stories(project_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        stories = stories_repo.get_stories_by_project(project_id)
        return message.success(stories, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET STORIES BY SPRINT FILTER
@app.route('/api/sprints/<int:sprint_id>/stories', methods=['GET'])
@jwt_required()
def get_sprint_stories(sprint_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        stories = stories_repo.get_stories_by_sprint(sprint_id)
        return message.success(stories, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ UPDATE STORY
@app.route('/api/stories/<int:story_id>', methods=['PUT'])
@jwt_required()
def update_story(story_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        story_points = data.get('story_points', 0)
        status = data.get('status')
        priority = data.get('priority')
        epic_id = data.get('epic_id')
        sprint_id = data.get('sprint_id') or data.get('sprintId')
        assignee_user_id = data.get('assignee_user_id')
        reporter_user_id = data.get('reporter_user_id')

        if not title or not status or not priority:
            return message.error({'error': 'title, status, and priority are required fields'}, 400)

        updated = stories_repo.update_story(
            story_id=story_id,
            title=title,
            description=description,
            story_points=story_points,
            status=status,
            priority=priority,
            epic_id=epic_id,
            sprint_id=sprint_id,
            assignee_user_id=assignee_user_id,
            reporter_user_id=reporter_user_id
        )

        if updated == 0:
            return message.error({'error': 'Story not found or no changes made'}, 404)

        return message.success({
            'id': story_id,
            'title': title,
            'status': status,
            'sprint_id': sprint_id,
            'story_points': story_points
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ DELETE STORY
@app.route('/api/stories/<int:story_id>', methods=['DELETE'])
@jwt_required()
def delete_story(story_id):
    try:
        user_email = get_jwt_identity()
        validators.UserFlowValidator.validate_email(user_email)

        deleted = stories_repo.delete_story(story_id)

        if deleted == 0:
            return message.error({'error': 'Story not found'}, 404)

        return message.success({
            'message': 'Story deleted successfully',
            'id': story_id
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)