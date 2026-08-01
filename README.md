# Workout Log API

A Flask-based REST API for logging workouts with session-based authentication. Built with Flask-SQLAlchemy, Flask-Bcrypt, and Flask-Migrate.

## Features

- User registration and login with secure password hashing
- Session-based authentication
- Full CRUD for workout logs
- Paginated workout listing
- SQLite database (easy to set up, no external DB server needed)

## Tech Stack

- **Flask** — web framework
- **Flask-SQLAlchemy** — ORM and database management
- **Flask-Migrate** — database migrations
- **Flask-Bcrypt** — password hashing
- **Flask-RESTful** — RESTful API structure
- **Flask-CORS** — cross-origin support (credentials included)

## Installation

### Prerequisites

- Python 3.13+
- [Pipenv](https://pipenv.pypa.io/)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/Ethanpaul1/Full-Auth-Flask-Backend--Productivity-App.git
cd Full-Auth-Flask-Backend--Productivity-App

# 2. Install dependencies
pipenv install

# 3. Activate the virtual environment
pipenv shell

# 4. Run database migrations
flask db upgrade

# 5. (Optional) Seed the database with test data
python seed.py

# 6. Start the server
python app.py
```

The API will be available at `http://localhost:5555`.

## API Endpoints

### Authentication

| Method | Endpoint    | Description                          | Auth Required |
|--------|-------------|--------------------------------------|---------------|
| POST   | `/signup`   | Register a new user                  | No            |
| POST   | `/login`    | Log in and create a session          | No            |
| DELETE | `/logout`   | Log out and clear the session        | Yes           |
| GET    | `/me`       | Return the currently logged-in user  | Yes           |

### Workouts

| Method | Endpoint           | Description                      | Auth Required |
|--------|--------------------|----------------------------------|---------------|
| GET    | `/workouts`        | List workouts (paginated)        | Yes           |
| POST   | `/workouts`        | Create a new workout             | Yes           |
| PATCH  | `/workouts/<id>`   | Update a workout (partial)       | Yes           |
| DELETE | `/workouts/<id>`   | Delete a workout                 | Yes           |

**Pagination query parameters for `GET /workouts`:**
- `page` — page number (default: `1`)
- `per_page` — items per page (default: `5`)

---

### Request / Response Examples

#### POST /signup

**Request:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "johndoe"
}
```

#### POST /login

**Request:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe"
}
```

#### GET /me

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe"
}
```

#### GET /workouts?page=1&per_page=5

**Response (200 OK):**
```json
{
  "workouts": [
    {
      "id": 1,
      "title": "Morning Run",
      "exercise_type": "Running",
      "duration_minutes": 30,
      "notes": "Felt great today",
      "date": "2026-01-15",
      "user_id": 1
    }
  ],
  "total": 12,
  "page": 1,
  "per_page": 5,
  "total_pages": 3
}
```

#### POST /workouts

**Request:**
```json
{
  "title": "Evening Yoga",
  "exercise_type": "Yoga",
  "duration_minutes": 45,
  "notes": "Relaxing session",
  "date": "2026-01-15"
}
```

**Response (201 Created):**
```json
{
  "id": 14,
  "title": "Evening Yoga",
  "exercise_type": "Yoga",
  "duration_minutes": 45,
  "notes": "Relaxing session",
  "date": "2026-01-15",
  "user_id": 1
}
```

#### PATCH /workouts/1

**Request:**
```json
{
  "duration_minutes": 35,
  "notes": "Updated notes"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Morning Run",
  "exercise_type": "Running",
  "duration_minutes": 35,
  "notes": "Updated notes",
  "date": "2026-01-15",
  "user_id": 1
}
```

#### DELETE /workouts/1

**Response:** `204 No Content`

---

## Status Codes

| Code | Description                        |
|------|------------------------------------|
| 200  | Success (GET, PATCH)               |
| 201  | Created (POST)                     |
| 204  | No Content (DELETE)                |
| 401  | Unauthorized — not logged in       |
| 403  | Forbidden — not your resource      |
| 404  | Not found                          |
| 422  | Unprocessable — validation failure |

## Database Models

### User

| Column         | Type     | Description                              |
|----------------|----------|------------------------------------------|
| `id`           | Integer  | Primary key                              |
| `username`     | String   | Unique username                          |
| `_password_hash` | String | Bcrypt hash (write-only, never exposed)  |

### Workout

| Column             | Type     | Description                              |
|--------------------|----------|------------------------------------------|
| `id`               | Integer  | Primary key                              |
| `title`            | String   | Workout title (e.g. "Morning Run")       |
| `exercise_type`    | String   | Type of exercise (e.g. "Running", "HIIT")|
| `duration_minutes` | Integer  | Duration in minutes                      |
| `notes`            | Text     | Optional notes                           |
| `date`             | String   | Date of workout (e.g. "2026-08-01")      |
| `user_id`          | Integer  | Foreign key to users table               |

## Seeded Test Data

After running `python seed.py`, the following test accounts are available:

| Username          | Password      |
|-------------------|---------------|
| michaelmorales    | password123   |
| mullenkaylee      | password123   |
| margaretpruitt    | password123   |

Each user has 5 sample workouts.
