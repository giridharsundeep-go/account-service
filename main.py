from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

# JWT Config
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

#Register controllers
from controllers.auth_controller import *
from controllers.org_controller import *

if __name__ == '__main__':
    app.run(debug=True, port=5000)