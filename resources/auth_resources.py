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


class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        # authenticate() runs bcrypt.check_password_hash internally
        if not user or not user.authenticate(password):
            return {'error': 'Invalid username or password.'}, 401

        session['user_id'] = user.id
        return user.to_dict(), 200


class Logout(Resource):
    def delete(self):
        # Return 401 if the user was not logged in to begin with
        if not session.get('user_id'):
            return {'error': 'Not logged in.'}, 401

        # Clear the session — the cookie still exists but user_id is now None
        session['user_id'] = None
        return {}, 204


class Me(Resource):
    """
    Check session endpoint — called by the frontend on every page refresh.
    Returns the logged-in user so the app does not redirect to /login unnecessarily.
    """
    def get(self):
        user_id = session.get('user_id')

        if not user_id:
            return {'error': 'Unauthorized.'}, 401

        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found.'}, 404

        return user.to_dict(), 200




