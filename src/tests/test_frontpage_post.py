import pytest
from flask import session
from flaskr.models import Frontpage_post

def test_frontpagePost(client, session):
    post = Frontpage_post(
        title="Firste post",
        author=1
    )
    session.add(post)
    session.commit()

    rs = client.get('post/{}'.format(post.id), follow_redirects=True)
    assert b'Firste post' in rs.data
    rs = client.get('post/999', follow_redirects=True)
    assert b'404' in rs.data