from flaskr.models import AdminUser
def test_add_admin(session):
    admin = AdminUser(username="test")

    session.add(admin)
    session.commit()
    print("teseeeeet")
    assert admin.id > 0
    assert 0 == 0
