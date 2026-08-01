from config import app, api
from resources.auth_resources import Signup, Login, Logout, Me
from resources.workout_resources import WorkoutList, WorkoutDetail

# ── Auth Routes ──────────────────────────────────────────────────────────────
api.add_resource(Signup, '/signup')   # POST   — register a new user
api.add_resource(Login,  '/login')    # POST   — log in
api.add_resource(Logout, '/logout')   # DELETE — log out (clear session)
api.add_resource(Me,     '/me')       # GET    — return current user (check session)

# ── Workout Routes ────────────────────────────────────────────────────────────
api.add_resource(WorkoutList,   '/workouts')          # GET, POST
api.add_resource(WorkoutDetail, '/workouts/<int:id>') # PATCH, DELETE

if __name__ == '__main__':
    app.run(debug=True, port=5555)

