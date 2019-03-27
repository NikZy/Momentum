import pytest
from flask import session
from flaskr.models import Job_position

def test_404(client):
    rs = client.get('/jobPosition/222/')
    assert b'404' in rs.data

def test_profile(client, session):
    position = Job_position(startup=1, title="first job position")
    session.add(position)
    session.commit()

    assert session.query(Job_position).filter_by(id=1).one_or_none()

    rs = client.get('/jobPosition/1/')
    assert rs.status_code == 200