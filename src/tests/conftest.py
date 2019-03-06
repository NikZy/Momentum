'''
The config for pytest. Should be ignored
'''
import os
import pytest

import flaskr.models
from flaskr import db as _db
import flaskr

from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))

TESTDB_PATH = os.path.join(basedir, 'test.db')
TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH

@pytest.fixture(scope='session')
def app(request):
    '''
    Create a Flask app context for the tests.
    '''
    app = flaskr.app

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TESTDB_PATH
    app.config['TESTING'] = True

    return app
@pytest.yield_fixture
def client(app):
    """A Flask test client. An instance of :class:`flask.testing.TestClient`
    by default.
    """
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='session')
def db(app, request):
    '''
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    '''
    #db = SQLAlchemy(app=app)
    from flaskr import models
    with app.app_context():
        _db.drop_all()
        _db.create_all()


    return db

@pytest.fixture(scope="function", autouse=True)
def session(app, db, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = _db.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = _db.create_scoped_session(options=options)

        # establish  a SAVEPOINT just before beginning the test
        # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
        sess.begin_nested()

        @event.listens_for(sess(), 'after_transaction_end')
        def restart_savepoint(sess2, trans):
            # Detecting whether this is indeed the nested transaction of the test
            if trans.nested and not trans._parent.nested:
                # The test should have normally called session.commit(),
                # but to be safe we explicitly expire the session
                sess2.expire_all()
                sess.begin_nested()

        _db.session = sess
        yield sess

        # Cleanup
        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()
        conn.close()

@pytest.fixture
def runner(app):
    '''
    The runner fixture is similar to client. app.test_cli_runner() creates a runner that can call the Click commands registered with the application.
    '''
