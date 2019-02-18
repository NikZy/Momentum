import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    '''
    Tester auth modellen.
    '''
    # assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a',
                                'password': 'a',
                                'mail': 'test@epost.no',
                                'type': 'admin'

                            }
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "select * from user where username= 'Sindre'",
        ).fetchone() is not None

# forteller pytest at den skal kjøre funksjonen under, med forkjellige parametere
@pytest.mark.parametrize(('username', 'password', 'mail', 'type', 'message'), (
    ('', '', '', '',  b'mangler obligatoriske felter'),
    ('guns', 'password', 'mail', 'job_applicant', b'already registered'),
))
def test_register_validate_input(client, username, password, mail, type, message):
    '''
    Tester gyldigheten av parametere til register funksjonen
    '''
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password, 'mail': mail, 'type':type}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    #assert response.headers['location'] == 'http://localhost/templates/index'

    with client:
        client.get('/')
        print(g.user)
        assert session['brukerid'] == 1
        assert g.bruker['brukernavn'] == 'guns'



@pytest.mark.parametrize(('brukernavn', 'passord', 'message'), (
    ('a', 'test', b'Feil brukernavn.'),
    ('test', 'a', b'Feil passord.'),
    ('a', '', b'Ikke noe passord.'),
))
def test_login_validate_input(auth, brukernavn, passord, message):
    response = auth.login(brukernavn, passord)
    assert message in response.data
