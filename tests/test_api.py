from app.models import User, Book, Loan, db


def login(client, email, password):
    return client.post("/login", data={"email": email, "password": password}, follow_redirects=True)


def create_user(app, role="member"):
    with app.app_context():
        user = User(email=f"{role}@example.com", name=role.title(), role=role)
        user.set_password("pass1234")
        db.session.add(user)
        db.session.commit()
        # return primitives to avoid detached instances outside the context
        return {"email": user.email, "password": "pass1234", "role": user.role}


def create_book(app, title="API Book", copies=1):
    with app.app_context():
        book = Book(title=title, author="Author", year=2024, language="EN", isbn=title, copies_total=copies, copies_available=copies)
        db.session.add(book)
        db.session.commit()
        return {"id": book.id, "title": book.title}


def test_api_books_requires_login(client):
    rv = client.get("/api/books")
    assert rv.status_code in (302, 401)


def test_api_books_list_and_create_permissions(client, app):
    member = create_user(app, "member")
    librarian = create_user(app, "librarian")
    create_book(app, "Existing")

    # member can read but not create
    login(client, member["email"], member["password"])
    rv = client.get("/api/books")
    assert rv.status_code == 200
    assert any(b["title"] == "Existing" for b in rv.get_json())

    rv = client.post("/api/books", json={"title": "New Title"})
    assert rv.status_code == 403

    # librarian can create
    client.get("/logout", follow_redirects=True)
    login(client, librarian["email"], librarian["password"])
    rv = client.post("/api/books", json={"title": "Created", "copies_total": 1, "copies_available": 1})
    assert rv.status_code == 201
    assert "id" in rv.get_json()


def test_api_checkout_and_return_flow(client, app):
    member = create_user(app, "member")
    book = create_book(app, "Loan Target")

    login(client, member["email"], member["password"])
    rv = client.post(f"/api/loans/{book['id']}/checkout")
    assert rv.status_code == 200
    payload = rv.get_json()
    assert "due_date" in payload
    loan_id = payload.get("loan_id") or payload.get("id")

    with app.app_context():
        refreshed_book = Book.query.get(book["id"])
        assert refreshed_book.copies_available == 0

    rv = client.post(f"/api/loans/{loan_id}/return")
    assert rv.status_code == 200
    assert rv.get_json().get("returned") is True

    with app.app_context():
        refreshed_book = Book.query.get(book["id"])
        refreshed_loan = Loan.query.get(loan_id)
        assert refreshed_book.copies_available == 1
        assert refreshed_loan.return_date is not None
