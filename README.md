# Flask Library Management System

A full‑stack Flask app for managing a small library: books, members, loans, search, and roles.

## Features
- Add/edit/delete books; track availability and checkouts
- Member registration, login, profiles
- Librarian/Admin roles with authorization guard
- Checkout/Return workflows with due dates & history
- Powerful search (title/author/language/year/ISBN)
- SQLite + SQLAlchemy + Flask-Migrate
- Bootstrap UI with Jinja templates
- REST-ish JSON API endpoints (documented in `docs/openapi.yaml`)
- Unit/integration tests via pytest

## Quickstart

### 1) Create & activate a virtualenv
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Set environment variables (development defaults)
Create a `.env` file (or export vars) like:
```
FLASK_APP=manage.py
FLASK_ENV=development
SECRET_KEY=dev-secret-change-me
DATABASE_URL=sqlite:///instance/library.db
```

### 4) Initialize the database
```bash
flask db upgrade
# seed an admin & sample data
python seed.py
```

### 5) Run
```bash
flask run
```
Open http://127.0.0.1:5000

### Default accounts (from `seed.py`)
- admin: `admin@example.com` / `adminpass` (role=admin)
- librarian: `librarian@example.com` / `librarianpass` (role=librarian)
- member: `member@example.com` / `memberpass` (role=member)

## Project Structure
```
flask_library_system/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── auth.py
│   ├── books.py
│   ├── users.py
│   ├── loans.py
│   ├── search.py
│   ├── api.py
│   ├── utils.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── books/
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   ├── form.html
│   │   ├── users/
│   │   │   ├── list.html
│   │   │   └── form.html
│   │   └── loans/
│   │       ├── list.html
│   │       └── history.html
│   └── static/
│       └── styles.css
├── instance/ (created at runtime)
├── manage.py
├── requirements.txt
├── seed.py
├── docs/
│   └── openapi.yaml
└── tests/
    ├── conftest.py
    ├── test_auth.py
    ├── test_books.py
    └── test_loans.py
```

## API Docs
See `docs/openapi.yaml`.

## Database Schema
- See `docs/schema.md` for table definitions and relationships.
- Defaults to SQLite; swap `DATABASE_URL` for other engines.

## Testing
```bash
pytest
```
Uses an in-memory SQLite database via the pytest fixtures in `tests/conftest.py`.

## Project Notes
- Roles: member, librarian, admin. Librarian/admin can manage books; admin manages users.
- Update the shared group spreadsheet with your team details (requires access to the Google Sheet).

## Coding Style
- PEP8 via `flake8`
- Type hints in core modules
