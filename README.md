# Flask Library Management System

A full-stack Flask application for managing books, members, and loans with role-based access control, a Bootstrap UI, and JSON endpoints.

## Features
- Manage books: add/edit/delete, track copies, availability, and details
- User auth: registration, login, session-based auth (Flask-Login)
- Roles: member, librarian, admin (librarian/admin manage books; admin manages users)
- Loans: checkout/return with due dates, personal loan list, global loan history
- Search: title/author/language/year/ISBN (UI and API)
- API: JSON endpoints documented in `docs/api.md`
- Testing: pytest unit/integration coverage for auth, books, loans

## Tech Stack
- Python, Flask, Flask-Login, Flask-WTF, Flask-SQLAlchemy
- SQLite (default) with SQLAlchemy ORM
- Bootstrap 5 (Jinja templates)
- pytest for testing

## Project Structure
```
flask_library_system/
├── app/
│   ├── __init__.py          # App factory, extensions, blueprints
│   ├── models.py            # SQLAlchemy models (User, Book, Loan)
│   ├── forms.py             # WTForms for auth/users/books
│   ├── auth.py              # Login/registration routes
│   ├── books.py             # Book CRUD + search UI
│   ├── users.py             # Admin user management
│   ├── loans.py             # Checkout/return/history UI
│   ├── search.py            # Advanced search UI
│   ├── api.py               # JSON endpoints
│   ├── utils.py             # Role decorator
│   ├── templates/           # Jinja templates
│   └── static/              # CSS
├── docs/
│   ├── api.md               # API reference (markdown)
│   └── openapi.yaml         # Legacy OpenAPI spec (optional)
├── tests/                   # pytest suites
├── manage.py                # Flask entrypoint + migrations hook
├── requirements.txt
└── seed.py                  # Demo data seeder (drops/recreates DB)
```

## Quickstart (fast path)
Prereqs: Python 3.10+, `pip`, `python3 -m venv`.

1) Clone and enter the project  
   ```bash
   git clone https://github.com/nadernima/flask-library-system.git
   cd flask-library-system
   ```
2) Create & activate a virtualenv  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3) Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```
4) Create the database with demo data (drops/recreates tables)  
   ```bash
   python seed.py
   ```
5) Run the app  
   ```bash
   flask run
   ```
   Open http://127.0.0.1:5000

That’s it. Login with the default accounts below.

## Configuration (optional)
You can skip this for local dev; sensible defaults are baked in. To customize, create a `.env` file:
```
FLASK_APP=manage.py
FLASK_ENV=development
SECRET_KEY=dev-secret-change-me
DATABASE_URL=sqlite:///instance/library.db   # defaults to sqlite:///library.db if unset
```

### Starting with an empty database (no demo data)
```bash
flask shell -c "from app import db, create_app; app=create_app(); app.app_context().push(); db.create_all()"
```

### Default Accounts (from `seed.py`)
- admin: `admin@example.com` / `adminpass`
- librarian: `librarian@example.com` / `librarianpass`
- member: `member@example.com` / `memberpass`

## Testing
```bash
pytest
```
Uses in-memory SQLite via fixtures (`tests/conftest.py`).

## API Documentation
- Markdown reference: `docs/api.md`

## Database Schema
See `docs/schema.md` for tables and relationships.

## Notes
- Roles: member, librarian, admin. Librarian/admin manage books; only admin manages users.
- `seed.py` will DROP existing tables before recreating; avoid running it on data you need to keep.
