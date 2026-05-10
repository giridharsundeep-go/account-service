from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.org_repository import OrganisationRepository
from repositories.user_account_repository import UserAccountRepository
from schemas.org_schemas import OrganisationSchema
from api_messages.common_messages import message

db = DatabaseConnectivity()
org_repo = OrganisationRepository(db)
user_repo = UserAccountRepository(db)
org_schema = OrganisationSchema()


# ✅ CREATE ORGANISATION (PROTECTED)
@app.route('/api/organisation/create', methods=['POST'])
@jwt_required()
def create_organisation():
    json_data = request.get_json()

    try:
        data = org_schema.load(json_data)
    except ValidationError as err:
        return message.error(err.messages, 400)

    user_email = get_jwt_identity()

    # ⚠️ You must map email → user_id
    # Ideally via repository (better design)
    # For now assuming email = user_id OR you fetch it

    user_id = user_email  # 🔁 replace with actual lookup if needed
    user = user_repo.get_user_by_email(user_id)
    if not user.get('email') == user_id:
        return message.error({'email': user_id}, 400)

    try:
        org_id = org_repo.create_organisation(data, user.get('id'))

        return message.success({
            "id": org_id,
            "title": data.get('title')
        }, "Organisation created successfully")

    except Exception as e:
        return message.error(str(e), 500)


# ✅ GET ORGANISATIONS (PROTECTED)
@app.route('/api/organisation/get', methods=['GET'])
@jwt_required()
def get_user_orgs():

    user_email = get_jwt_identity()
    user_id = user_email  # 🔁 map properly in real system

    user = user_repo.get_user_by_email(user_id)
    if not user.get('email') == user_id:
        return message.error({'email': user_id}, 400)

    try:
        orgs = org_repo.get_user_orgs(user.get('id'))
        return message.success(orgs)

    except Exception as e:
        return message.error(str(e), 500)

# ✅ GET ORGANISATION (PROTECTED)
@app.route('/api/organisation/get/<int:org_id>', methods=['GET'])
@jwt_required()
def get_organisation(org_id):

    user_email = get_jwt_identity()

    user = user_repo.get_user_by_email(user_email)
    if not user or user.get('email') != user_email:
        return message.error({'email': user_email}, 400)

    try:
        org = org_repo.get_org(org_id)

        if not org:
            return message.error(f'Organisation with id {org_id} not found', 404)

        return message.success(org)

    except Exception as e:
        return message.error(str(e), 500)