from flask import render_template
from auth import require_role
from database import get_db


@require_role("user")
def member_dashboard(decoded):
    db = get_db()
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("member/dashboard.html", user=decoded["user"], books=books)
