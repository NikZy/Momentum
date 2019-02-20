import os
import pytest

#import flaskr
#from flaskr import db as _db
from flask import Flask
from db_test import db as _db
# from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

TESTDB_PATH = os.path.join(basedir, 'test.db')
TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH

@pytest.fixture(scope='session')
def database(request):
    '''
    Create a Postgres database for the tests, and drop it when the tests are done.
    '''
    pg_host = DB_OPTS.get("host")
    pg_port = DB_OPTS.get("port")
    pg_user = DB_OPTS.get("username")
    pg_db = DB_OPTS["database"]

    init_postgresql_database(pg_user, pg_host, pg_port, pg_db)

    @request.addfinalizer
    def drop_database():
        drop_postgresql_database(pg_user, pg_host, pg_port, pg_db, 9.6)

@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI
    }
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["TEST_DATABASE_URI"] = TEST_DATABASE_URI
    app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app

def apply_migrations():
    """Applies all alembic migrations."""
    config = Config(ALEMBIC_CONFIG)
    upgrade(config, 'head')

@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)

    def teardown():
        _db.drop_all()
        os.unlink(TESTDB_PATH)

    _db.app = app
    apply_migrations()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
