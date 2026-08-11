import os
import time
from contextlib import contextmanager

import mysql.connector
from flask import Flask, jsonify, render_template, request, session
from mysql.connector import Error, errorcode
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-me-in-production")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "mysql"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "appuser"),
    "password": os.getenv("DB_PASSWORD", "apppassword"),
    "database": os.getenv("DB_NAME", "auth_demo"),
}


@contextmanager
def db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    last_error = None
    for _ in range(30):
        try:
            with db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(80) NOT NULL UNIQUE,
                        email VARCHAR(255) NOT NULL UNIQUE,
                        password_hash VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                conn.commit()
                cursor.close()
                return
        except Error as exc:
            last_error = exc
            time.sleep(2)

    raise RuntimeError(f"Database did not become ready: {last_error}")


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/me")
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"authenticated": False})

    with db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, username, email, created_at FROM users WHERE id = %s",
            (user_id,),
        )
        user = cursor.fetchone()
        cursor.close()

    if not user:
        session.clear()
        return jsonify({"authenticated": False})

    return jsonify({"authenticated": True, "user": user})


@app.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters."}), 400
    if "@" not in email or "." not in email:
        return jsonify({"error": "Enter a valid email address."}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    password_hash = generate_password_hash(password)

    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                """,
                (username, email, password_hash),
            )
            conn.commit()
            user_id = cursor.lastrowid
            cursor.close()
    except Error as exc:
        if exc.errno == errorcode.ER_DUP_ENTRY:
            return jsonify({"error": "Username or email already exists."}), 409
        return jsonify({"error": "Could not create your account."}), 500

    session["user_id"] = user_id
    return jsonify(
        {
            "message": "Account created.",
            "user": {"id": user_id, "username": username, "email": email},
        }
    ), 201


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    identifier = (data.get("identifier") or "").strip()
    password = data.get("password") or ""

    if not identifier or not password:
        return jsonify({"error": "Email or username and password are required."}), 400

    with db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, username, email, password_hash
            FROM users
            WHERE email = %s OR username = %s
            """,
            (identifier.lower(), identifier),
        )
        user = cursor.fetchone()
        cursor.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid login details."}), 401

    session["user_id"] = user["id"]
    return jsonify(
        {
            "message": "Logged in.",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
            },
        }
    )


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out."})


init_db()
