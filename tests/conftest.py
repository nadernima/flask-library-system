import os, tempfile, pytest
from app import create_app, db

@pytest.fixture()
def app():
    # Use a temp SQLite DB for tests
    os.environ["DATABASE_URL"] = "sqlite://"
    os.environ["SECRET_KEY"] = "test"
    test_app = create_app()
    test_app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
