from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .models import User
from .forms import UserForm
from . import db
from .utils import roles_required

users_bp = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")

@users_bp.route("/")
@login_required
@roles_required("librarian","admin")
def list_users():
    users = User.query.order_by(User.name.asc()).all()
    return render_template("users/list.html", users=users)

@users_bp.route("/new", methods=["GET","POST"])
@login_required
@roles_required("admin")
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, role=form.role.data)
        user.set_password("changeme123")
        db.session.add(user)
        db.session.commit()
        flash("User created (temp password 'changeme123').", "success")
        return redirect(url_for("users.list_users"))
    return render_template("users/form.html", form=form)

@users_bp.route("/<int:user_id>/edit", methods=["GET","POST"])
@login_required
@roles_required("admin")
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash("User updated.", "success")
        return redirect(url_for("users.list_users"))
    return render_template("users/form.html", form=form)
