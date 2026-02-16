# Workout Tracker

A mobile-first workout tracking app built with Flask and SQLite.

## Features

- **Programs** - Create workout programs (collections of workouts)
- **Workouts** - Build workouts from exercises with custom sets, reps, weight
- **Exercises** - Track strength (reps/weight) and cardio (duration) exercises
- **Logging** - Log workouts with tap-to-complete set tracking
- **Progress** - View exercise progress and personal records
- **History** - Browse workout history with calendar view
- **PWA** - Works offline with service worker caching

## Setup

### Requirements
- Python 3.10+
- pip

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
flask db upgrade

# Run development server
python run.py
```

The app will be available at `http://localhost:8888`

## Usage

1. **Register** an account
2. **Create a Program** (e.g., "Push/Pull/Legs")
3. **Create Workouts** (e.g., "Push", "Pull", "Legs")
4. **Add Exercises** to workouts (sets, reps, weight)
5. **Reorder Workouts** in your program
6. **Start Workouts** from the home page
7. **Track Sets** by tapping set circles
8. **View Progress** by clicking exercises in history

## Tech Stack

- **Backend** - Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login
- **Database** - SQLite
- **Frontend** - Jinja2 templates, vanilla JavaScript
- **Mobile** - PWA with service worker, responsive CSS
- **Auth** - bcrypt password hashing, session-based login

## Development

Run tests:
```bash
pytest
```

Start with debug mode:
```bash
python run.py
```
