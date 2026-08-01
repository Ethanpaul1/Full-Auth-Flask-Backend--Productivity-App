from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)

# SQLite database stored in instance/workout_log.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_log.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key signs the session cookie — keep this private in production
app.config['SECRET_KEY'] = 'super-secret-key-change-in-production'

# supports_credentials=True allows session cookies to be sent cross-origin
# (needed so the frontend on a different port can stay logged in)
CORS(app, supports_credentials=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)

