from flask import request, session
from flask_restful import Resource
from models import Workout
from config import db


def get_current_user_id():
    """
    Helper function — reads the logged-in user's ID from the session.
    Returns None if there is no active session.
    """
    return session.get('user_id')


class WorkoutList(Resource):
    def get(self):
        """
        GET /workouts
        Returns a paginated list of workouts belonging to the logged-in user only.
        Accepts optional query params: ?page=1&per_page=5
        """
        user_id = get_current_user_id()
        if not user_id:
            return {'error': 'Unauthorized. Please log in.'}, 401

        # Read pagination params from the URL query string — default to page 1, 5 per page
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # filter_by(user_id=user_id) ensures users only see their own workouts
        paginated = (
            Workout.query
            .filter_by(user_id=user_id)
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        return {
            'workouts': [w.to_dict() for w in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': paginated.page,
        }, 200

