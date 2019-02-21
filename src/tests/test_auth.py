from flaskr.models import AdminUser, set_password, check_password
import pytest

def test_add_admin_and_set_password(session):
    admin = AdminUser(username="test")

    set_password(admin, "test123")
    assert check_password(admin, "test") == False
    assert check_password(admin, "test123") == True

    session.add(admin)
    session.commit() # save to DB

    assert admin.id > 0
    assert AdminUser.query.filter_by(username='test').first() is not None


def test_register(client):
    response = client.get('/auth/register')
    assert response.status_code == 200
    
@pytest.mark.parametrize(('name', 'email', 'password','type', 'message'), (
    ('', '', '','jobbsøker', b'mangler obligatoriske felter'),
    #('Sindre', 'sindre@sivertsen.no', 'passord123', 'bruker finnes fra før'),
))
def test_register_jobbsøker_validate_input(client, name, email, password, type, message):
    response = client.post('/auth/register', data={'name': name, 'email':email, 'type': type, 'password':password})

    assert message in response.data
