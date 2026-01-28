from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    g,
)
import jwt, datetime, sqlite3, bcrypt
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret-key"


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()


@app.route("/dashboard")
def dashboard():
    token = request.cookies.get("access_token")
    decoded = decode_jwt(token) if token else None
    if not decoded:
        return redirect(url_for("login"))
    return render_template(
        "dashboard.html", user=decoded["user"], role=decoded["role"], token=token
    )


@app.route("/admin")
@require_role("admin")
def admin_panel(decoded):
    return render_template("admin.html", user=decoded["user"])


@app.route("/base")
def base():
    return render_template("base.html")


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login")))
    resp.delete_cookie("access_token")
    return resp


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
