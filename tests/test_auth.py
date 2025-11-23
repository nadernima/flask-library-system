from app.models import User, db

def test_register_and_login(client, app):
    # Register
    rv = client.post('/register', data={
        'name':'Test User', 'email':'test@example.com', 'password':'secret123'
    }, follow_redirects=True)
    assert rv.status_code == 200

    # Login
    rv = client.post('/login', data={
        'email':'test@example.com', 'password':'secret123'
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Welcome back" in rv.data or b"Logged in" in rv.data
