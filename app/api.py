from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from .models import Book, Loan, User
from . import db

api_bp = Blueprint("api", __name__)

def require_librarian():
    if not current_user.is_authenticated or not current_user.is_librarian():
        abort(403)

@api_bp.get("/books")
@login_required
def api_list_books():
    q = request.args.get("q","")
    query = Book.query
    if q:
        like = f"%{q}%"
        query = query.filter((Book.title.ilike(like)) | (Book.author.ilike(like)))
    books = query.all()
    return jsonify([{
        "id": b.id, "title": b.title, "author": b.author, "year": b.year,
        "language": b.language, "isbn": b.isbn, "copies_available": b.copies_available
    } for b in books])

@api_bp.post("/books")
@login_required
def api_create_book():
    require_librarian()
    data = request.get_json() or {}
    b = Book(
        title=data.get("title"),
        author=data.get("author"),
        year=data.get("year"),
        language=data.get("language"),
        isbn=data.get("isbn"),
        description=data.get("description"),
        copies_total=data.get("copies_total", 1),
        copies_available=data.get("copies_available", 1),
    )
    db.session.add(b)
    db.session.commit()
    return jsonify({"id": b.id}), 201

@api_bp.post("/loans/<int:book_id>/checkout")
@login_required
def api_checkout(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.copies_available:
        return jsonify({"error": "No copies available"}), 400
    loan = Loan(user_id=current_user.id, book_id=book.id, due_date=Loan.default_due())
    book.copies_available -= 1
    db.session.add(loan)
    db.session.commit()
    return jsonify({"loan_id": loan.id, "due_date": loan.due_date.isoformat()})

@api_bp.post("/loans/<int:loan_id>/return")
@login_required
def api_return(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    if loan.user_id != current_user.id and not current_user.is_librarian():
        abort(403)
    loan.return_date = loan.return_date or db.func.now()
    loan.book.copies_available += 1
    db.session.commit()
    return jsonify({"returned": True})
