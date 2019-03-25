'''
TODO 

'''
from flaskr.models import Startup, Tag
from flask import session
import pytest
from flaskr import search

def test_search_page(client):
    response = client.get('/search')
    assert response.status_code == 200 or response.status_code == 301

def test_search_queries(client, session):
    startup = Startup(email="startup@startup.no", name="startup")
    tag1 = Tag(tagname="testtag")
    startup.tags.append(tag1)
    session.add(tag1)
    session.add(startup)
    session.commit()

    assert session.query(Startup).filter_by(email="startup@startup.no").one_or_none()

    # search
    data = {
        "search-input": "startup",
        "testtag": "on",
    }
    response = client.post('/search', data=data, follow_redirects=True)
    search.search()
    print(response.data)
    assert b'startup' in response.data
    assert b'testtag' in response.data
    
    response = client.post('/search', data={'search-input': "lajlasjdaslh"}, follow_redirects=True)
    assert b'Ingen treff' in response.data



