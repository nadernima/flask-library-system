from app.models import User, Book, Loan, db

def login(client, email, password):
    return client.post('/login', data={'email':email,'password':password}, follow_redirects=True)

def setup_member_and_book(app):
    with app.app_context():
        u = User(email="member@example.com", name="Member", role="member")
        u.set_password("pass1234")
        b = Book(title="Loanable", author="A", year=2020, language="EN", isbn="x", copies_total=1, copies_available=1)
        db.session.add_all([u,b]); db.session.commit()
        return {"email": u.email, "password": "pass1234", "id": u.id}, {"id": b.id}

def test_checkout_and_return(client, app):
    u, b = setup_member_and_book(app)
    login(client, u["email"], u["password"])
    rv = client.get(f"/loans/checkout/{b['id']}", follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get("/loans/")  # list loans
    assert b"Loanable" in rv.data

    with app.app_context():
        loan = Loan.query.filter_by(user_id=u["id"], book_id=b["id"]).first()
        assert loan is not None
        assert loan.return_date is None
        assert Book.query.get(b["id"]).copies_available == 0
        loan_id = loan.id

    rv = client.get(f"/loans/return/{loan_id}", follow_redirects=True)
    assert rv.status_code == 200

    with app.app_context():
        updated_loan = Loan.query.get(loan_id)
        updated_book = Book.query.get(b["id"])
        assert updated_loan.return_date is not None
        assert updated_book.copies_available == 1
