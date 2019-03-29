from flaskr.models import Startup, Job_applicant, Job_position
from flask import session
import pytest

def test_seed_data(session):
    startup1 = Startup(email="testStartup@lol.no", name="test")
    job_applicant = Job_applicant(email="ja@ja.no", first_name="testJobApplicant", last_name="lastname")
    job_position = Job_position(title="test_job_position", startup=1)

    session.add_all([startup1, job_applicant, job_position])
    session.commit()
    assert True
def test_profile_startup(client):
    rs = client.get('profile/startup/1', follow_redirects=True)
    assert rs.status_code == 200
    assert b'testStartup@lol.no' in rs.data
    rs = client.get('profile/startup/999', follow_redirects=True)
    assert b'404' in rs.data

def test_profile_startup_job_position(client):
    rs = client.get('profile/startup/1/job_position/1', follow_redirects=True)
    assert rs.status_code == 200
    rs = client.get('profile/startup/1/job_position/1212', follow_redirects=True)
    assert b'404' in rs.data

def test_register_job_position(client, session):
    data = {
        'title': 'new_position',
        'deadline': '1995-01-01',
        'contact_mail': 'mail@mail.no',
        'startup': '1'
    }
    rs = client.post('/profile/startup/1/register_job_position', data=data, follow_redirects=True)
    assert rs.status_code == 200



def test_profile_job_applicant(client):
    rs = client.get('profile/job_applicant/1', follow_redirects=True)
    assert rs.status_code == 200

    rs = client.get('profile/job_applicant/9999', follow_redirects=True)
    assert b'404' in rs.data

