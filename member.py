from flask import Blueprint, render_template
from auth import require_role
from database import get_db

member_bp = Blueprint("member", __name__, template_folder="templates/member")


@member_bp.route("/dashboard")
@require_role("user")
def member_dashboard(decoded):
    db = get_db()
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template(
        "member/dashboard.html", user=decoded["user"], role=decoded["role"], books=books
    )


@member_bp.route("/books")
@require_role("user")
def member_books(decoded):
    db = get_db()
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template(
        "member/books.html", user=decoded["user"], role=decoded["role"], books=books
    )
