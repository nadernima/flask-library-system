from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Book, Loan, User
from . import db
from .utils import roles_required

loans_bp = Blueprint("loans", __name__, url_prefix="/loans", template_folder="templates")

@loans_bp.route("/")
@login_required
def my_loans():
    loans = Loan.query.filter_by(user_id=current_user.id).order_by(Loan.checkout_date.desc()).all()
    return render_template("loans/list.html", loans=loans)

@loans_bp.route("/history")
@login_required
@roles_required("librarian","admin")
def history():
    loans = Loan.query.order_by(Loan.checkout_date.desc()).all()
    return render_template("loans/history.html", loans=loans)

@loans_bp.route("/checkout/<int:book_id>")
@login_required
def checkout(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.available():
        flash("No copies available.", "warning")
        return redirect(url_for("books.detail", book_id=book.id))
    loan = Loan(user_id=current_user.id, book_id=book.id, due_date=Loan.default_due())
    book.copies_available -= 1
    db.session.add(loan)
    db.session.commit()
    flash("Book checked out!", "success")
    return redirect(url_for("loans.my_loans"))

@loans_bp.route("/return/<int:loan_id>")
@login_required
def return_book(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    if loan.user_id != current_user.id and not current_user.is_librarian() and not current_user.is_admin():
        flash("Not allowed.", "danger")
        return redirect(url_for("loans.my_loans"))
    if loan.return_date:
        flash("Already returned.", "info")
        return redirect(url_for("loans.my_loans"))
    loan.return_date = datetime.utcnow()
    loan.book.copies_available += 1
    db.session.commit()
    flash("Book returned. Thank you!", "success")
    return redirect(url_for("loans.my_loans"))
