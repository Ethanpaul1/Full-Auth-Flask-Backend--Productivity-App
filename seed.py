from config import app, db
from models import User, Workout
from faker import Faker

fake = Faker()

EXERCISE_TYPES = ['Running', 'Cycling', 'Swimming', 'Weight Training', 'Yoga', 'HIIT', 'Pilates']

with app.app_context():
    print("Clearing existing data...")
    db.drop_all()
    db.create_all()

    print("Seeding users...")
    users = []
    for _ in range(3):
        user = User(username=fake.unique.user_name())
        # Uses the password_hash setter which runs bcrypt before storing
        user.password_hash = 'password123'
        db.session.add(user)
        users.append(user)

    db.session.commit()

    print("Seeding workouts...")
    for user in users:
        for _ in range(5):
            workout = Workout(
                title=f"{fake.random_element(EXERCISE_TYPES)} Session",
                exercise_type=fake.random_element(EXERCISE_TYPES),
                duration_minutes=fake.random_int(min=15, max=90),
                notes=fake.sentence(nb_words=10),
                date=str(fake.date_this_year()),
                user_id=user.id,
            )
            db.session.add(workout)

    db.session.commit()

    print(f"Done! Seeded {len(users)} users and {len(users) * 5} workouts.")
    print("\nTest login credentials (all passwords are 'password123'):")
    for u in users:
        print(f"  username: {u.username}")

