from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from sqlalchemy.orm import relationship, validates

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="member")  # member|librarian|admin
    password_hash = db.Column(db.String(255), nullable=False)
    loans = relationship("Loan", back_populates="user", lazy="dynamic")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def is_admin(self): return self.role == "admin"
    def is_librarian(self): return self.role in ("librarian", "admin")

    @validates("role")
    def validate_role(self, key, value):
        assert value in ("member", "librarian", "admin")
        return value

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    author = db.Column(db.String(255), index=True)
    year = db.Column(db.Integer, index=True)
    language = db.Column(db.String(10), index=True)
    isbn = db.Column(db.String(32), unique=True, index=True)
    description = db.Column(db.Text)
    copies_total = db.Column(db.Integer, default=1)
    copies_available = db.Column(db.Integer, default=1)
    loans = relationship("Loan", back_populates="book", lazy="dynamic")

    def available(self) -> bool:
        return self.copies_available > 0

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False, index=True)
    checkout_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)

    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")

    def is_returned(self):
        return self.return_date is not None

    @staticmethod
    def default_due():
        return datetime.utcnow() + timedelta(days=14)
