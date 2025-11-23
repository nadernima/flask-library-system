from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required
from .models import Book, Loan
from .forms import BookForm
from . import db
from .utils import roles_required

books_bp = Blueprint("books", __name__, url_prefix="/books", template_folder="templates")

@books_bp.route("/")
@login_required
def list_books():
    q = request.args.get("q","").strip()
    query = Book.query
    if q:
        like = f"%{q}%"
        query = query.filter((Book.title.ilike(like)) | (Book.author.ilike(like)) | (Book.language.ilike(like)) | (Book.isbn.ilike(like)))
    books = query.order_by(Book.title.asc()).all()
    return render_template("books/list.html", books=books, q=q)

@books_bp.route("/new", methods=["GET","POST"])
@login_required
@roles_required("librarian","admin")
def create_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book()
        form.populate_obj(book)
        db.session.add(book)
        db.session.commit()
        flash("Book added.", "success")
        return redirect(url_for("books.list_books"))
    return render_template("books/form.html", form=form, mode="create")

@books_bp.route("/<int:book_id>")
@login_required
def detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("books/detail.html", book=book)

@books_bp.route("/<int:book_id>/edit", methods=["GET","POST"])
@login_required
@roles_required("librarian","admin")
def edit(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        flash("Book updated.", "success")
        return redirect(url_for("books.detail", book_id=book.id))
    return render_template("books/form.html", form=form, mode="edit", book=book)

@books_bp.route("/<int:book_id>/delete", methods=["POST"])
@login_required
@roles_required("librarian","admin")
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    loans_exist = Loan.query.filter_by(book_id=book.id).count()
    if loans_exist:
        flash("Cannot delete: book has loan history. Remove related loans first.", "warning")
        return redirect(url_for("books.detail", book_id=book.id))
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted.", "info")
    return redirect(url_for("books.list_books"))
