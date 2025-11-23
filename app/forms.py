from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Create account")

class BookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[Optional()])
    year = IntegerField("Year", validators=[Optional(), NumberRange(min=0, max=9999)])
    language = StringField("Language", validators=[Optional(), Length(max=10)])
    isbn = StringField("ISBN", validators=[Optional(), Length(max=32)])
    description = TextAreaField("Description", validators=[Optional()])
    copies_total = IntegerField("Total copies", validators=[DataRequired(), NumberRange(min=1)])
    copies_available = IntegerField("Available copies", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Save")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = SelectField("Role", choices=[("member","Member"),("librarian","Librarian"),("admin","Admin")], validators=[DataRequired()])
    submit = SubmitField("Save")
