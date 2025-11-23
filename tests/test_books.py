from app.models import Book, User, Loan, db

def login(client, email, password):
    return client.post('/login', data={'email':email,'password':password}, follow_redirects=True)

def create_user(app, role="librarian"):
    with app.app_context():
        u = User(email=f"{role}@example.com", name=role.title(), role=role)
        u.set_password("pass1234")
        db.session.add(u); db.session.commit()
        return {"email": u.email, "password": "pass1234", "id": u.id}

def test_book_crud(client, app):
    # create librarian
    librarian = create_user(app, "librarian")
    login(client, librarian["email"], librarian["password"])

    # create book
    rv = client.post('/books/new', data={
        'title':'Test Book','author':'Anon','year':2021,'language':'EN','isbn':'123',
        'description':'X','copies_total':2,'copies_available':2
    }, follow_redirects=True)
    assert rv.status_code == 200

    # list shows it
    assert b"Test Book" in rv.data


def test_librarian_can_delete_book(client, app):
    librarian = create_user(app, "librarian")
    with app.app_context():
        book = Book(title="Delete Me", author="X", copies_total=1, copies_available=1)
        db.session.add(book); db.session.commit()
        book_id = book.id

    login(client, librarian["email"], librarian["password"])
    rv = client.post(f"/books/{book_id}/delete", follow_redirects=True)
    assert rv.status_code == 200

    with app.app_context():
        assert Book.query.get(book_id) is None


def test_delete_blocked_when_active_loan(client, app):
    librarian = create_user(app, "librarian")
    with app.app_context():
        user = User(email="member2@example.com", name="Member2", role="member")
        user.set_password("pass1234")
        book = Book(title="On Loan", author="Y", copies_total=1, copies_available=0)
        db.session.add_all([user, book]); db.session.commit()
        loan = Loan(user_id=user.id, book_id=book.id, due_date=Loan.default_due())
        db.session.add(loan); db.session.commit()
        book_id = book.id

    login(client, librarian["email"], librarian["password"])
    rv = client.post(f"/books/{book_id}/delete", follow_redirects=True)
    assert rv.status_code == 200
    assert b"Cannot delete" in rv.data
    with app.app_context():
        assert Book.query.get(book_id) is not None


def test_delete_blocked_when_historical_loan(client, app):
    librarian = create_user(app, "librarian")
    with app.app_context():
        user = User(email="member3@example.com", name="Member3", role="member")
        user.set_password("pass1234")
        book = Book(title="History Book", author="Z", copies_total=1, copies_available=1)
        db.session.add_all([user, book]); db.session.commit()
        loan = Loan(user_id=user.id, book_id=book.id, due_date=Loan.default_due(), return_date=Loan.default_due())
        db.session.add(loan); db.session.commit()
        book_id = book.id

    login(client, librarian["email"], librarian["password"])
    rv = client.post(f"/books/{book_id}/delete", follow_redirects=True)
    assert rv.status_code == 200
    assert b"loan history" in rv.data
    with app.app_context():
        assert Book.query.get(book_id) is not None
