from config import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # unique=True means no two users can share a username — required for login to work
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Leading underscore marks this as internal — never access it directly from outside the model
    _password_hash = db.Column(db.String(128), nullable=False)

    # cascade='all, delete-orphan' means deleting a user also deletes all their workouts
    workouts = db.relationship('Workout', back_populates='user', cascade='all, delete-orphan')

    @property
    def password_hash(self):
        # Raise an error if someone tries to read the hash — it should never be exposed
        raise AttributeError('Password hashes are write-only.')

    @password_hash.setter
    def password_hash(self, plain_text_password):
        # bcrypt turns the plain text password into a secure hash before storing it
        self._password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def authenticate(self, plain_text_password):
        # Compares the plain text input against the stored hash — returns True or False
        return bcrypt.check_password_hash(self._password_hash, plain_text_password)

    def to_dict(self):
        # Safe serialization — never include _password_hash here
        return {'id': self.id, 'username': self.username}


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)         # e.g. "Morning Run"
    exercise_type = db.Column(db.String(50), nullable=False)  # e.g. "Running", "HIIT"
    duration_minutes = db.Column(db.Integer, nullable=False)  # e.g. 45
    notes = db.Column(db.Text)                                 # optional free-text
    date = db.Column(db.String(20))                            # e.g. "2026-08-01"

    # Foreign key links each workout to exactly one user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='workouts')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'exercise_type': self.exercise_type,
            'duration_minutes': self.duration_minutes,
            'notes': self.notes,
            'date': self.date,
            'user_id': self.user_id,
        }


