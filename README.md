# Cybersecurity Awareness Training Platform
Flask + SQLite Software Engineering project.

Student: Login -> Courses -> Quiz -> Result -> Certificate
Trainer: Login -> Training content -> Student results
Admin: Login -> Users -> Courses -> Reports

Run:
python -m venv .venv
python -m pip install -r requirements.txt
python app.py

Open http://127.0.0.1:5000

This is an educational demo. Production should add secure authentication, password hashing, CSRF protection and secure secret management.
