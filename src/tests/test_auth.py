import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    '''
    Tester auth modellen.
    '''
    # assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'brukernavn': 'a', 
                                'passord': 'a',
                                'epost': 'test@epost.no',
                                'type': 'admin'

                            }
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "select * from bruker where brukernavn= 'Sindre'",
        ).fetchone() is not None

# forteller pytest at den skal kjøre funksjonen under, med forkjellige parametere
@pytest.mark.parametrize(('brukernavn', 'passord', 'epost', 'type', 'message'), (
    ('', '', '', '',  b'mangler obligatoriske felter'),
    ('guns', 'passord', 'epost', 'jobbsøker', b'already registered'),
))
def test_register_validate_input(client, brukernavn, passord, epost, type, message):
    '''
    Tester gyldigheten av parametere til register funksjonen
    '''
    response = client.post(
        '/auth/register',
        data={'brukernavn': brukernavn, 'passord': passord, 'epost': epost, 'type':type}
    )
    assert message in response.data


def test_login(client, auth):
    # assert client.get('/auth/login').status_code == 200
    response = auth.login()
    # assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
       #  assert session['user_id'] == 1
       # assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    # assert message in response.data
