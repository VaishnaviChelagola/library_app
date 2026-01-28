from flask import render_template, request, redirect, url_for
from auth import require_role
from database import get_db


@require_role("admin")
def admin_dashboard(decoded):
    return render_template("admin/dashboard.html", user=decoded["user"])


@require_role("admin")
def add_book(decoded):
    db = get_db()
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        if not title or not author:
            books = db.execute("SELECT * FROM books").fetchall()
            return render_template(
                "admin/books.html",
                user=decoded["user"],
                books=books,
                error="All fields required",
            )
        db.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        db.commit()
        return redirect(url_for("admin_books"))

    # GET request: show all books
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("admin/books.html", user=decoded["user"], books=books)
