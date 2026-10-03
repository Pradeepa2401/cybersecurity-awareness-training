from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

import sqlite3
import os
from functools import wraps
from datetime import datetime


# =========================================================
# FLASK CONFIGURATION
# =========================================================

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

if os.environ.get("VERCEL"):
    DB = "/tmp/cybersecurity.db"
else:
    DB = os.path.join(app.root_path, "cybersecurity.db")


# =========================================================
# COURSES
# =========================================================

COURSES = [
    (
        "Password Security",
        "Learn strong passwords, MFA, and account protection."
    ),
    (
        "Phishing Awareness",
        "Recognize suspicious emails, links, messages, and attachments."
    ),
    (
        "Safe Internet Practices",
        "Learn safer browsing, updates, downloads, and public Wi-Fi habits."
    ),
    (
        "Social Media Safety",
        "Protect privacy and personal information online."
    ),
    (
        "Social Engineering Awareness",
        "Understand manipulation tactics and safe verification."
    ),
    (
        "Mobile & Device Security",
        "Learn device protection, updates, permissions, and backups."
    )
]


# =========================================================
# QUIZZES
# =========================================================

QUIZZES = {

    "Password Security": [
        (
            "What is a strong password practice?",
            "Use a unique password for each important account",
            [
                "Use the same password everywhere",
                "Share passwords with friends",
                "Use your birthday as a password"
            ]
        ),
        (
            "Why should you avoid reusing passwords?",
            "A compromised password could put multiple accounts at risk",
            [
                "It makes passwords shorter",
                "It makes websites load slower",
                "It removes the need for updates"
            ]
        ),
        (
            "What does MFA provide?",
            "An additional verification step",
            [
                "A faster internet connection",
                "Automatic password sharing",
                "A larger storage space"
            ]
        ),
        (
            "Which password should you avoid?",
            "A simple password based on easily known personal information",
            [
                "A long unique password",
                "A unique password for each account",
                "A securely stored password"
            ]
        ),
        (
            "What should you do if you think your password was exposed?",
            "Change it and follow the account's security guidance",
            [
                "Share it with a friend",
                "Keep using it",
                "Post it online"
            ]
        )
    ],

    "Phishing Awareness": [
        (
            "Which is a common sign of phishing?",
            "A message creating unusual urgency and asking for sensitive information",
            [
                "A normal school timetable",
                "A saved offline document",
                "A normal offline note"
            ]
        ),
        (
            "What should you do with a suspicious link?",
            "Avoid opening it and verify the message through a trusted channel",
            [
                "Open it immediately",
                "Forward it to everyone",
                "Enter your password first"
            ]
        ),
        (
            "Why should unexpected attachments be treated carefully?",
            "They may contain unsafe or unwanted content",
            [
                "They always improve computer speed",
                "They are always harmless",
                "They automatically update your device"
            ]
        ),
        (
            "What is a safe response to an unexpected account request?",
            "Verify the request using a trusted method",
            [
                "Reply immediately",
                "Share your password",
                "Post the request publicly"
            ]
        ),
        (
            "What should you do when a message seems suspicious?",
            "Check the sender and verify the request before responding",
            [
                "Click every link",
                "Send personal information",
                "Ignore all security checks"
            ]
        )
    ],

    "Safe Internet Practices": [
        (
            "Why are software updates important?",
            "They can include security fixes and improvements",
            [
                "They always remove all files",
                "They guarantee zero risk",
                "They are only for changing wallpaper"
            ]
        ),
        (
            "What should you check before entering information on a website?",
            "Make sure the website address and connection are appropriate",
            [
                "The number of advertisements",
                "The page color",
                "The font size"
            ]
        ),
        (
            "What is a safer approach to downloads?",
            "Download software from trusted sources",
            [
                "Use any random download site",
                "Disable all security features",
                "Download unknown files immediately"
            ]
        ),
        (
            "What should you do when using public Wi-Fi?",
            "Be careful with sensitive activities and use appropriate security measures",
            [
                "Share passwords publicly",
                "Disable all device security",
                "Trust every network automatically"
            ]
        ),
        (
            "Why should browsers be kept updated?",
            "Updates can include security improvements",
            [
                "They remove the keyboard",
                "They prevent all websites from loading",
                "They guarantee complete online safety"
            ]
        )
    ],

    "Social Media Safety": [
        (
            "Why should privacy settings be reviewed?",
            "They help control who can access shared information",
            [
                "They increase battery size",
                "They remove the internet",
                "They guarantee no one can contact you"
            ]
        ),
        (
            "What should you avoid sharing publicly?",
            "Sensitive personal information",
            [
                "A general hobby",
                "A favorite subject",
                "A general interest"
            ]
        ),
        (
            "What should you do with an unfamiliar account request?",
            "Check the account before accepting",
            [
                "Accept every request",
                "Share your password",
                "Send private information"
            ]
        ),
        (
            "Why is oversharing risky?",
            "It can expose information that others could misuse",
            [
                "It improves account security",
                "It prevents scams",
                "It automatically protects your account"
            ]
        ),
        (
            "What is a good social media security practice?",
            "Use strong account security settings",
            [
                "Share login details",
                "Use the same password everywhere",
                "Turn off every security feature"
            ]
        )
    ],

    "Social Engineering Awareness": [
        (
            "What is social engineering?",
            "Manipulating people into revealing information or taking an action",
            [
                "Updating software",
                "Backing up files",
                "Changing screen brightness"
            ]
        ),
        (
            "What should you do with an unusual request for confidential information?",
            "Verify the request using a trusted method",
            [
                "Share it immediately",
                "Post it publicly",
                "Forward it to strangers"
            ]
        ),
        (
            "Why can urgency be a warning sign?",
            "It may pressure someone into acting without checking",
            [
                "It always means the request is genuine",
                "It improves security",
                "It prevents mistakes"
            ]
        ),
        (
            "What should you do if someone claims to be an authority and asks for sensitive information?",
            "Independently verify their identity and request",
            [
                "Give the information immediately",
                "Share your password",
                "Ignore all security practices"
            ]
        ),
        (
            "What is an important defense against social engineering?",
            "Pause, verify, and think before responding",
            [
                "Always respond immediately",
                "Share confidential information",
                "Trust every unexpected request"
            ]
        )
    ],

    "Mobile & Device Security": [
        (
            "Why should devices be updated?",
            "Updates can include important security fixes",
            [
                "They guarantee zero risk",
                "They remove all applications",
                "They only change wallpapers"
            ]
        ),
        (
            "Why should a screen lock be used?",
            "It helps prevent unauthorized access to the device",
            [
                "It increases internet speed",
                "It removes malware automatically",
                "It shares your files"
            ]
        ),
        (
            "Where should applications preferably be installed from?",
            "Trusted and official sources",
            [
                "Unknown websites",
                "Random links",
                "Unverified files"
            ]
        ),
        (
            "Why should app permissions be reviewed?",
            "Some applications may request access they do not need",
            [
                "It makes the phone heavier",
                "It disables all apps",
                "It guarantees unlimited storage"
            ]
        ),
        (
            "Why are backups useful?",
            "They can help recover important information if data is lost",
            [
                "They prevent every possible attack",
                "They increase screen brightness",
                "They remove the need for updates"
            ]
        )
    ]
}


# =========================================================
# DATABASE CONNECTION
# =========================================================

def db():
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    return connection


# =========================================================
# DATABASE INITIALIZATION + OLD DATABASE FIX
# =========================================================

def init_db():

    c = db()

    # -----------------------------------------------------
    # USERS
    # -----------------------------------------------------

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    # -----------------------------------------------------
    # RESULTS
    # -----------------------------------------------------

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    # -----------------------------------------------------
    # PROGRESS
    # -----------------------------------------------------

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course TEXT NOT NULL,
            completed_at TEXT,
            UNIQUE(user_id, course)
        )
        """
    )

    # -----------------------------------------------------
    # QUIZ QUESTIONS
    # -----------------------------------------------------

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT NOT NULL,
            question TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            wrong_answer1 TEXT NOT NULL,
            wrong_answer2 TEXT NOT NULL,
            wrong_answer3 TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    # Seed the database with the original quiz bank only once.
    # After that, Trainer add/remove actions are stored in SQLite.
    question_count = c.execute(
        "SELECT COUNT(*) FROM quiz_questions"
    ).fetchone()[0]

    if question_count == 0:

        for course_title, quiz_questions in QUIZZES.items():

            for question, correct_answer, wrong_answers in quiz_questions:

                c.execute(
                    """
                    INSERT INTO quiz_questions
                    (
                        course,
                        question,
                        correct_answer,
                        wrong_answer1,
                        wrong_answer2,
                        wrong_answer3,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        course_title,
                        question,
                        correct_answer,
                        wrong_answers[0],
                        wrong_answers[1],
                        wrong_answers[2],
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                )

    # -----------------------------------------------------
    # FIX OLD DATABASE
    # -----------------------------------------------------
    # Your old progress table may not contain completed_at.
    # CREATE TABLE IF NOT EXISTS does not update an existing
    # table, so we check and add the column if necessary.

    columns = c.execute(
        "PRAGMA table_info(progress)"
    ).fetchall()

    column_names = [
        column["name"]
        for column in columns
    ]

    if "completed_at" not in column_names:

        c.execute(
            """
            ALTER TABLE progress
            ADD COLUMN completed_at TEXT
            """
        )

        # Give existing completed courses a date.
        c.execute(
            """
            UPDATE progress
            SET completed_at = ?
            WHERE completed_at IS NULL
            """,
            (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            )
        )

    c.commit()
    c.close()


# Initialize the database when the app is imported (required by Vercel).
init_db()


# =========================================================
# LOGIN REQUIRED
# =========================================================

def login_required(roles=None):

    def decorator(view):

        @wraps(view)
        def wrapped(*args, **kwargs):

            if not session.get("user_id"):

                flash(
                    "Please login first.",
                    "error"
                )

                return redirect(
                    url_for("login")
                )

            if roles:

                current_role = session.get("role")

                if current_role not in roles:

                    flash(
                        "You do not have permission to access this page.",
                        "error"
                    )

                    return redirect(
                        url_for("dashboard")
                    )

            return view(*args, **kwargs)

        return wrapped

    return decorator


# =========================================================
# LOGIN
# =========================================================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        role = request.form.get(
            "role",
            ""
        ).strip()

        allowed_roles = [
            "Student",
            "Trainer",
            "Admin"
        ]

        if not name:

            flash(
                "Please enter your name.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        if role not in allowed_roles:

            flash(
                "Please select a valid role.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        c = db()

        user = c.execute(
            """
            SELECT *
            FROM users
            WHERE name = ? AND role = ?
            """,
            (name, role)
        ).fetchone()

        if user is None:

            cur = c.execute(
                """
                INSERT INTO users
                (name, role, created_at)
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    role,
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
            )

            user_id = cur.lastrowid

            c.commit()

            user = c.execute(
                """
                SELECT *
                FROM users
                WHERE id = ?
                """,
                (user_id,)
            ).fetchone()

        c.close()

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["role"] = user["role"]

        session.pop("last_result_id", None)
        session.pop("last_quiz_course", None)
        session.pop("last_quiz_index", None)

        return redirect(
            url_for("dashboard")
        )

    return render_template("login.html")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required()
def dashboard():

    c = db()

    user = c.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (session["user_id"],)
    ).fetchone()

    completed = 0
    total_courses = len(COURSES)
    attempts = 0
    result = None

    if user["role"] == "Student":

        completed_row = c.execute(
            """
            SELECT COUNT(*) AS count
            FROM progress
            WHERE user_id = ?
            """,
            (session["user_id"],)
        ).fetchone()

        completed = completed_row["count"]

        attempts_row = c.execute(
            """
            SELECT COUNT(*) AS count
            FROM results
            WHERE user_id = ?
            """,
            (session["user_id"],)
        ).fetchone()

        attempts = attempts_row["count"]

        result = c.execute(
            """
            SELECT *
            FROM results
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (session["user_id"],)
        ).fetchone()

    c.close()

    return render_template(
        "dashboard.html",
        user=user,
        completed=completed,
        total_courses=total_courses,
        attempts=attempts,
        result=result
    )


# =========================================================
# COURSES
# =========================================================

@app.route("/courses")
@login_required(["Student"])
def courses():

    c = db()

    rows = c.execute(
        """
        SELECT course
        FROM progress
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchall()

    c.close()

    progress = {}

    for row in rows:
        progress[row["course"]] = True

    return render_template(
        "courses.html",
        courses=COURSES,
        progress=progress
    )


# =========================================================
# COMPLETE COURSE
# =========================================================

@app.route(
    "/course/<int:index>/complete",
    methods=["POST"]
)
@login_required(["Student"])
def complete_course(index):

    if not 0 <= index < len(COURSES):

        flash(
            "Course not found.",
            "error"
        )

        return redirect(
            url_for("courses")
        )

    course_title = COURSES[index][0]

    c = db()

    c.execute(
        """
        INSERT OR IGNORE INTO progress
        (user_id, course, completed_at)
        VALUES (?, ?, ?)
        """,
        (
            session["user_id"],
            course_title,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    c.commit()
    c.close()

    flash(
        f"{course_title} marked as completed.",
        "success"
    )

    return redirect(
        url_for("courses")
    )


# =========================================================
# QUIZ
# =========================================================

@app.route(
    "/quiz/<int:index>",
    methods=["GET", "POST"]
)
@login_required(["Student"])
def quiz(index):

    if not 0 <= index < len(COURSES):

        flash(
            "Course not found.",
            "error"
        )

        return redirect(
            url_for("courses")
        )

    course_title = COURSES[index][0]

    c = db()

    rows = c.execute(
        """
        SELECT
            question,
            correct_answer,
            wrong_answer1,
            wrong_answer2,
            wrong_answer3
        FROM quiz_questions
        WHERE course = ?
        ORDER BY id
        """,
        (course_title,)
    ).fetchall()

    c.close()

    questions = [
        (
            row["question"],
            row["correct_answer"],
            [
                row["wrong_answer1"],
                row["wrong_answer2"],
                row["wrong_answer3"]
            ]
        )
        for row in rows
    ]

    if not questions:

        flash(
            "Quiz is not available for this course.",
            "error"
        )

        return redirect(
            url_for("courses")
        )

    if request.method == "POST":

        # -------------------------------------------------
        # CHECK ALL QUESTIONS ARE ANSWERED
        # -------------------------------------------------

        unanswered = []

        for i in range(len(questions)):

            selected_answer = request.form.get(
                f"q{i}"
            )

            if not selected_answer:
                unanswered.append(i + 1)

        if unanswered:

            flash(
                "Please answer all questions before submitting the quiz.",
                "error"
            )

            return render_template(
                "quiz.html",
                questions=questions,
                course_title=course_title
            )

        # -------------------------------------------------
        # CALCULATE SCORE
        # -------------------------------------------------

        score = 0

        for i, question in enumerate(questions):

            selected_answer = request.form.get(
                f"q{i}"
            )

            correct_answer = question[1]

            if selected_answer == correct_answer:
                score += 1

        total = len(questions)

        # -------------------------------------------------
        # SAVE RESULT
        # -------------------------------------------------

        c = db()

        cur = c.execute(
            """
            INSERT INTO results
            (
                user_id,
                score,
                total,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                session["user_id"],
                score,
                total,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )

        result_id = cur.lastrowid

        c.commit()
        c.close()

        # -------------------------------------------------
        # STORE LAST QUIZ
        # -------------------------------------------------

        session["last_result_id"] = result_id
        session["last_quiz_course"] = course_title
        session["last_quiz_index"] = index

        return redirect(
            url_for("result")
        )

    return render_template(
        "quiz.html",
        questions=questions,
        course_title=course_title
    )


# =========================================================
# RESULT
# =========================================================

@app.route("/result")
@login_required(["Student"])
def result():

    result_id = session.get(
        "last_result_id"
    )

    if not result_id:

        return render_template(
            "result.html",
            result=None,
            quiz_index=None
        )

    c = db()

    result_row = c.execute(
        """
        SELECT *
        FROM results
        WHERE id = ? AND user_id = ?
        """,
        (
            result_id,
            session["user_id"]
        )
    ).fetchone()

    c.close()

    if not result_row:

        flash(
            "Result not found.",
            "error"
        )

        return redirect(
            url_for("courses")
        )

    quiz_index = session.get(
        "last_quiz_index"
    )

    return render_template(
        "result.html",
        result=result_row,
        quiz_index=quiz_index
    )


# =========================================================
# CERTIFICATE
# 60% OR ABOVE ONLY
# =========================================================

@app.route("/certificate")
@login_required(["Student"])
def certificate():

    result_id = session.get(
        "last_result_id"
    )

    if not result_id:

        flash(
            "Complete a quiz before viewing a certificate.",
            "error"
        )

        return redirect(
            url_for("courses")
        )

    c = db()

    result_row = c.execute(
        """
        SELECT *
        FROM results
        WHERE id = ? AND user_id = ?
        """,
        (
            result_id,
            session["user_id"]
        )
    ).fetchone()

    c.close()

    if not result_row:

        flash(
            "Result not found.",
            "error"
        )

        return redirect(
            url_for("courses")
        )

    score = result_row["score"]
    total = result_row["total"]

    if total <= 0:

        flash(
            "Invalid quiz result.",
            "error"
        )

        return redirect(
            url_for("courses")
        )

    percentage = (
        score / total
    ) * 100

    # -----------------------------------------------------
    # CERTIFICATE REQUIREMENT
    # -----------------------------------------------------

    if percentage < 60:

        flash(
            "Certificate is available only for scores of 60% or above.",
            "error"
        )

        return redirect(
            url_for("result")
        )

    return render_template(
        "certificate.html",
        result=result_row,
        percentage=round(percentage),
        user=session.get("user_name")
    )


# =========================================================
# TRAINER
# =========================================================

@app.route("/trainer")
@login_required(["Trainer"])
def trainer():

    c = db()

    questions = c.execute(
        """
        SELECT *
        FROM quiz_questions
        ORDER BY course, id
        """
    ).fetchall()

    c.close()

    return render_template(
        "trainer.html",
        courses=COURSES,
        questions=questions
    )


@app.route("/trainer/questions/add", methods=["POST"])
@login_required(["Trainer"])
def trainer_add_question():

    course = request.form.get("course", "").strip()
    question = request.form.get("question", "").strip()
    correct_answer = request.form.get("correct_answer", "").strip()
    wrong_answer1 = request.form.get("wrong_answer1", "").strip()
    wrong_answer2 = request.form.get("wrong_answer2", "").strip()
    wrong_answer3 = request.form.get("wrong_answer3", "").strip()

    valid_courses = [title for title, _ in COURSES]

    if course not in valid_courses:
        flash("Please select a valid course.", "error")
        return redirect(url_for("trainer"))

    if not all([
        question,
        correct_answer,
        wrong_answer1,
        wrong_answer2,
        wrong_answer3
    ]):
        flash("Please fill in every question field.", "error")
        return redirect(url_for("trainer"))

    c = db()

    c.execute(
        """
        INSERT INTO quiz_questions
        (
            course,
            question,
            correct_answer,
            wrong_answer1,
            wrong_answer2,
            wrong_answer3,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            course,
            question,
            correct_answer,
            wrong_answer1,
            wrong_answer2,
            wrong_answer3,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    c.commit()
    c.close()

    flash("Question added successfully.", "success")
    return redirect(url_for("trainer"))


@app.route("/trainer/questions/<int:question_id>/delete", methods=["POST"])
@login_required(["Trainer"])
def trainer_delete_question(question_id):

    c = db()

    row = c.execute(
        "SELECT id FROM quiz_questions WHERE id = ?",
        (question_id,)
    ).fetchone()

    if row is None:
        c.close()
        flash("Question not found.", "error")
        return redirect(url_for("trainer"))

    c.execute(
        "DELETE FROM quiz_questions WHERE id = ?",
        (question_id,)
    )

    c.commit()
    c.close()

    flash("Question removed successfully.", "success")
    return redirect(url_for("trainer"))


@app.route("/trainer/results")
@login_required(["Trainer"])
def trainer_results():

    c = db()

    results = c.execute(
        """
        SELECT
            results.id,
            users.name,
            results.score,
            results.total,
            results.created_at
        FROM results
        JOIN users
        ON users.id = results.user_id
        WHERE users.role = 'Student'
        ORDER BY results.id DESC
        """
    ).fetchall()

    c.close()

    return render_template(
        "trainer_results.html",
        results=results
    )


# =========================================================
# ADMIN
# =========================================================

@app.route("/admin")
@login_required(["Admin"])
def admin():

    c = db()

    users = c.execute(
        """
        SELECT *
        FROM users
        ORDER BY id DESC
        """
    ).fetchall()

    results = c.execute(
        """
        SELECT
            results.id,
            users.name,
            users.role,
            results.score,
            results.total,
            results.created_at
        FROM results
        JOIN users
        ON users.id = results.user_id
        ORDER BY results.id DESC
        """
    ).fetchall()

    student_count = c.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE role = 'Student'
        """
    ).fetchone()[0]

    trainer_count = c.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE role = 'Trainer'
        """
    ).fetchone()[0]

    admin_count = c.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE role = 'Admin'
        """
    ).fetchone()[0]

    total_attempts = c.execute(
        """
        SELECT COUNT(*)
        FROM results
        """
    ).fetchone()[0]

    c.close()

    return render_template(
        "admin.html",
        users=users,
        results=results,
        student_count=student_count,
        trainer_count=trainer_count,
        admin_count=admin_count,
        total_attempts=total_attempts,
        courses=COURSES
    )


# =========================================================
# ADMIN PLATFORM OVERVIEW
# =========================================================

@app.route("/admin/overview")
@login_required(["Admin"])
def admin_overview():

    c = db()

    users = c.execute(
        """
        SELECT *
        FROM users
        ORDER BY id DESC
        """
    ).fetchall()

    results = c.execute(
        """
        SELECT
            results.id,
            users.name,
            results.score,
            results.total,
            results.created_at
        FROM results
        JOIN users
        ON users.id = results.user_id
        WHERE users.role = 'Student'
        ORDER BY results.id DESC
        """
    ).fetchall()

    total_attempts = c.execute(
        """
        SELECT COUNT(*)
        FROM results
        """
    ).fetchone()[0]

    c.close()

    return render_template(
        "admin_overview.html",
        users=users,
        results=results,
        total_attempts=total_attempts,
        courses=COURSES
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
