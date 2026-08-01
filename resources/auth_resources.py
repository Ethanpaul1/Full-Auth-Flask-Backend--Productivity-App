from flask import request, session
from flask_restful import Resource
from models import User
from config import db


class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Validate both fields are present before touching the database
        if not username or not password:
            return {'error': 'Username and password are required.'}, 422

        # Check for duplicate username before trying to insert
        if User.query.filter_by(username=username).first():
            return {'error': 'Username already taken.'}, 422

        user = User(username=username)
        # Triggers the password_hash setter which runs bcrypt
        user.password_hash = password
        db.session.add(user)
        db.session.commit()

        # Log the user in immediately by storing their ID in the session cookie
        session['user_id'] = user.id
        return user.to_dict(), 201

