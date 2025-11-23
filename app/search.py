from flask import Blueprint, request, render_template
from flask_login import login_required
from .models import Book

search_bp = Blueprint("search", __name__, url_prefix="/search", template_folder="templates")

@search_bp.route("/")
@login_required
def search():
    title = request.args.get("title")
    author = request.args.get("author")
    language = request.args.get("language")
    year = request.args.get("year", type=int)

    query = Book.query
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if language:
        query = query.filter(Book.language.ilike(f"%{language}%"))
    if year:
        query = query.filter(Book.year == year)

    results = query.order_by(Book.title.asc()).all()
    return render_template("books/list.html", books=results, q="")
