from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from marshmallow import Schema, fields, ValidationError
import mysql.connector
import re

app = Flask(__name__)
CORS(app, supports_credentials=True)

# ===== CONFIG =====
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ===== MYSQL CONFIG =====
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Mysql0707",
    database="professy_db"
)

cursor = db.cursor(dictionary=True)

# ===== VALIDATORS =====
def validate_username(value):
    email_regex = r'^[^@]+@[^@]+\.[^@]+$'
    phone_regex = r'^[0-9]{10}$'
    if not (re.match(email_regex, value) or re.match(phone_regex, value)):
        raise ValidationError("Must be valid email or phone")

def validate_password(value):
    if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{6,}$', value):
        raise ValidationError("Weak password")

# ===== SCHEMAS =====
class SignupSchema(Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    gender = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate_password)

class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate_username)
    password = fields.Str(required=True)

signup_schema = SignupSchema()
login_schema = LoginSchema()

def success(data=None, message="Success"):
    return jsonify({"success": True, "message": message, "data": data}), 200

def error(message="Error", code=400):
    return jsonify({"success": False, "message": message}), code

@app.route('/api/auth/create-account', methods=['POST'])
def signup():
    json_data = request.get_json()

    try:
        data = signup_schema.load(json_data)
    except ValidationError as err:
        return error(err.messages, 400)

    cursor.execute(
        "SELECT * FROM user_account WHERE email=%s OR phone=%s",
        (data['email'], data['phone'])
    )
    existing = cursor.fetchone()

    if existing:
        return error("User already exists", 409)

    hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    cursor.execute("""
        INSERT INTO user_account 
        (first_name, last_name, email, phone, gender, password)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data['firstName'],
        data['lastName'],
        data['email'],
        data['phone'],
        data['gender'],
        hashed
    ))

    db.commit()

    return success(message="Account created successfully")

# ===== LOGIN =====
@app.route('/api/auth/login', methods=['POST'])
def login():
    json_data = request.get_json()

    try:
        data = login_schema.load(json_data)
    except ValidationError as err:
        return error(err.messages, 400)

    username = data['username']
    password = data['password']

    cursor.execute(
        "SELECT * FROM user_account WHERE email=%s OR phone=%s",
        (username, username)
    )
    user = cursor.fetchone()

    if not user:
        return error("Invalid username or password", 401)

    if not bcrypt.check_password_hash(user['password'], password):
        return error("Invalid username or password", 401)

    token = create_access_token(identity=user['id'])

    # update last login
    cursor.execute(
        "UPDATE user_account SET last_login = NOW() WHERE id=%s",
        (user['id'],)
    )
    db.commit()

    return success({
        "token": token,
        "user": {
            "name": user['first_name'] + " " + user['last_name'],
            "email": user['email']
        }
    }, "Login successful")


if __name__ == '__main__':
    app.run(debug=True, port=5000)