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

    def post(self):
        """
        POST /workouts
        Creates a new workout for the logged-in user.
        Required body fields: title, exercise_type, duration_minutes
        """
        user_id = get_current_user_id()
        if not user_id:
            return {'error': 'Unauthorized. Please log in.'}, 401

        data = request.get_json()
        title = data.get('title')
        exercise_type = data.get('exercise_type')
        duration_minutes = data.get('duration_minutes')

        # Validate required fields before writing to the database
        if not title or not exercise_type or not duration_minutes:
            return {'error': 'title, exercise_type, and duration_minutes are required.'}, 422

        workout = Workout(
            title=title,
            exercise_type=exercise_type,
            duration_minutes=duration_minutes,
            notes=data.get('notes', ''),
            date=data.get('date', ''),
            user_id=user_id,
        )
        db.session.add(workout)
        db.session.commit()
        return workout.to_dict(), 201


class WorkoutDetail(Resource):
    def patch(self, id):
        """
        PATCH /workouts/<id>
        Updates a workout by ID.
        Only the owner of the workout can update it — returns 403 otherwise.
        """
        user_id = get_current_user_id()
        if not user_id:
            return {'error': 'Unauthorized. Please log in.'}, 401

        workout = Workout.query.get(id)
        if not workout:
            return {'error': 'Workout not found.'}, 404

        # 403 Forbidden — you are authenticated but this is not your workout
        if workout.user_id != user_id:
            return {'error': 'Forbidden. You can only edit your own workouts.'}, 403

        data = request.get_json()
        # Only update fields that were actually sent in the request body
        for field in ['title', 'exercise_type', 'duration_minutes', 'notes', 'date']:
            if field in data:
                setattr(workout, field, data[field])

        db.session.commit()
        return workout.to_dict(), 200

    def delete(self, id):
        """
        DELETE /workouts/<id>
        Deletes a workout by ID.
        Only the owner of the workout can delete it — returns 403 otherwise.
        """
        user_id = get_current_user_id()
        if not user_id:
            return {'error': 'Unauthorized. Please log in.'}, 401

        workout = Workout.query.get(id)
        if not workout:
            return {'error': 'Workout not found.'}, 404

        if workout.user_id != user_id:
            return {'error': 'Forbidden. You can only delete your own workouts.'}, 403

        db.session.delete(workout)
        db.session.commit()
        return {}, 204




