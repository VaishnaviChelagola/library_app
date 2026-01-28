from flask import Blueprint, render_template, request, redirect, url_for
from auth import require_role
from database import get_db

admin_bp = Blueprint("admin", __name__, template_folder="templates/admin")


@admin_bp.route("/dashboard")
@require_role("admin")
def admin_dashboard(decoded):
    return render_template("dashboard.html", user=decoded["user"], role=decoded["role"])


@admin_bp.route("/books", methods=["GET", "POST"])
@require_role("admin")
def admin_books(decoded):
    db = get_db()
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        if not title or not author:
            books = db.execute("SELECT * FROM books").fetchall()
            return render_template(
                "books.html",
                user=decoded["user"],
                books=books,
                error="All fields required",
            )
        db.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        db.commit()
        return redirect(url_for("admin.admin_books"))

    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", user=decoded["user"], books=books)
