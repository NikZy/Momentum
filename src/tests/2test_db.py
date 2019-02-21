import sqlite3
from flaskr.db import get_db
import pytest

def test_get_glose_db(app):
    '''
    Tester om det går an å åpne og lukke databasen
    '''
    with app.app_context():
        db = get_db()
        assert db is get_db()
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    
    assert 'closed' in str(e)


def test_init_db_command(runner, monkeypatch):
    '''
    Tester "flask init-db" kommandoen
    '''
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called