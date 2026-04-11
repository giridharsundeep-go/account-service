from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token

from main import app, bcrypt
from database_connectivity import DatabaseConnectivity
from repositories.user_repository import UserRepository
from schemas.user_flow_schemas import SignupSchema, LoginSchema
from api_messages import common_messages

db = DatabaseConnectivity()
user_repo = UserRepository(db)


# ✅ SIGNUP
@app.route('/api/auth/create-account', methods=['POST'])
def signup():
    json_data = request.get_json()

    try:
        data = SignupSchema().load(json_data)
    except ValidationError as err:
        return common_messages.message.error(err.messages, 400)

    existing = user_repo.get_user(data['email'], data['phone'])

    if existing:
        return common_messages.message.error("User already exists", 409)

    hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user_repo.create_user(data, hashed)

    return common_messages.message.success(message="Account created successfully")


# ✅ LOGIN
@app.route('/api/auth/login', methods=['POST'])
def login():
    json_data = request.get_json()

    try:
        data = LoginSchema().load(json_data)
    except ValidationError as err:
        return common_messages.message.error(err.messages, 400)

    user = user_repo.get_user_by_email(data['email'])

    if not user:
        return common_messages.message.error("User not found", 404)

    if not bcrypt.check_password_hash(user['password'], data['password']):
        return common_messages.message.error("Invalid credentials", 401)

    # ✅ JWT Token
    access_token = create_access_token(identity=user['email'])

    return common_messages.message.success({
        "token": access_token,
        "user": user
    }, "Login successful")