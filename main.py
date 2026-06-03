from flask import Flask, make_response
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200"])

# JWT Config
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.before_request
def allow_options_requests():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:4200"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response, 200

#Register controllers
from controllers.auth_controller import *
from controllers.org_controller import *
from controllers.roles_controller import *
from controllers.user_controller import *
from controllers.teams_controller import teams_bp
from controllers.team_members_controller import *
from controllers.projects_controller import *
from controllers.project_teams_controller import *
from controllers.projects_individual_members_controller import *
from controllers.products_controller import *
from controllers.sprints_controller import *
from controllers.epics_controller import *
from controllers.stories_controller import *
from controllers.tasks_controller import *

if __name__ == '__main__':
    app.run(debug=True, port=5000)