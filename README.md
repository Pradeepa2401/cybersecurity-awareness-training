# Cybersecurity Awareness Training Platform

Flask + SQLite Software Engineering project for cybersecurity awareness training.

## Features

- Student: Login → Courses → Quiz → Result → Certificate
- Trainer: Login → Training Content → Student Results
- Admin: Login → Users → Courses → Reports

## Run

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python app.py
Open: http://127.0.0.1:5000

## Note

This is an educational demo. Production deployment should add secure authentication, password hashing, CSRF protection, and secure secret management.
