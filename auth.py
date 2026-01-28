from flask import (
    request,
    render_template,
    redirect,
    url_for,
    make_response,
    current_app as app,
    abort,
)
import sqlite3, bcrypt, jwt, datetime
from functools import wraps
from database import get_db

DB = "library.db"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")  # admin / user

        if not username or not password or not role:
            return render_template("register.html", error="All fields are required")

        if role not in ("admin", "user"):
            return render_template("register.html", error="Invalid role")

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        try:
            with sqlite3.connect(DB) as db:
                cur = db.cursor()
                cur.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, hashed, role),
                )
                db.commit()
        except sqlite3.IntegrityError:
            return render_template("register.html", error="User already exists")

        return redirect(url_for("login"))

    return render_template("register.html")


def create_jwt(user, role):
    payload = {
        "user": user,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
    }

    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    return token


def decode_jwt(token):
    try:
        return jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None


def require_role(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = request.cookies.get("access_token")
            if not token:
                return redirect(url_for("login"))
            decoded = decode_jwt(token)
            if not decoded or decoded["role"] != role:
                abort(403)
            return fn(decoded, *args, **kwargs)

        return wrapper

    return decorator


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=?", (username,)
        ).fetchone()

        if user and bcrypt.checkpw(password, user["password"]):
            token = create_jwt(user["username"], user["role"])
            resp = make_response(redirect(url_for("dashboard")))
            resp.set_cookie("access_token", token, httponly=True, samesite="Lax")
            return resp

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")
