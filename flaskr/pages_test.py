from flaskr import create_app
from flask_login import FlaskLoginClient
from flaskr.user import User
from unittest.mock import patch
from io import BytesIO

import pytest


# See https://flask.palletsprojects.com/en/2.2.x/testing/
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })

    # we need this so we can login during tests using fake users
    app.test_client_class = FlaskLoginClient

    return app


# for when we want anonymous user :|
@pytest.fixture
def anon_client(app):
    return app.test_client()


def test_home_get(anon_client):
    resp = anon_client.get("/")
    assert resp.status_code == 200
    assert b"Hello fellow sussy bakas!" in resp.data


def test_upload_get__logged_out(anon_client):
    resp = anon_client.get("/upload", follow_redirects=True)
    assert b'''Please log in to access this page.''' in resp.data


def test_upload_get__logged_in(anon_client):
    with anon_client:
        resp1 = anon_client.post("/login",
                                 data=dict(username='testtest',
                                           password='testtest'),
                                 follow_redirects=True)

        assert b'''Hello there testtest!''' in resp1.data

        resp = anon_client.get("/upload", follow_redirects=True)
        # assert resp.status_code == 200
        assert b'''Post Title''' in resp.data


@patch('flaskr.pages.backend')
def test_upload_post_logged_in(backendMock, anon_client):
    backendMock.upload.return_value = "test name"

    with anon_client:
        resp1 = anon_client.post("/login",
                                 data=dict(username='testtest',
                                           password='testtest'),
                                 follow_redirects=True)

        assert b'''Hello there testtest!''' in resp1.data

        resp = anon_client.post("/upload",
                                data=dict(
                                    post_title='idk',
                                    content='idk',
                                    post_image=(BytesIO(b'my file contents'),
                                                "work_order.123")),
                                follow_redirects=True)
        # assert resp.status_code == 200
        assert b'''Success! See at''' in resp.data


def test_upload_post_logged_out(anon_client):
    resp = anon_client.post("/upload", follow_redirects=True)
    assert b'''Please log in to access this page''' in resp.data


def test_about_get(anon_client):
    resp = anon_client.get("/about", follow_redirects=True)
    assert b'''About this Wiki''' in resp.data


# this could be better with mocking
def test_pages_get(anon_client):
    resp = anon_client.get("/pages/", follow_redirects=True)
    assert b'''Emergency Meeting''' in resp.data


@patch('flaskr.pages.backend')
def test_pages2_get__exist(backendMock, anon_client):
    backendMock.get_wiki_page.return_value = "roblox"

    resp = anon_client.get("/pages/roblox/", follow_redirects=True)
    assert b'''roblox''' in resp.data


@patch('flaskr.pages.backend')
def test_pages2_get__nonexist(backendMock, anon_client):
    backendMock.get_wiki_page.return_value = None

    resp = anon_client.get("/pages/roblox/", follow_redirects=True)
    assert b'''URL was not found on the server''' in resp.data


def test_signup_get(anon_client):
    resp = anon_client.get("/signup", follow_redirects=True)
    assert b'''Create your sussy account''' in resp.data


@patch('flaskr.pages.backend')
def test_signup_post__success(mockBackendClass, anon_client):
    mockBackendClass.sign_up.return_value = None

    resp = anon_client.post("/signup",
                            data=dict(username='testtest', password='testtest'),
                            follow_redirects=True)
    assert b'''SUCCESFULL''' in resp.data


@patch('flaskr.pages.backend')
def test_signup_post__invalid(mockBackendClass, anon_client):
    mockBackendClass.sign_up.return_value = 'INVALID'

    resp = anon_client.post("/signup",
                            data=dict(username='testtest', password='testtest'),
                            follow_redirects=True)
    assert b'''Create your sussy account''' in resp.data


@patch('flaskr.pages.backend')
def test_signup_post__already_exist(mockBackendClass, anon_client):
    mockBackendClass.sign_up.return_value = 'ALREADY EXISTS'

    resp = anon_client.post("/signup",
                            data=dict(username='testtest', password='testtest'),
                            follow_redirects=True)
    assert b'''Create your sussy account''' in resp.data


def test_login_get__logged_out(anon_client):
    resp = anon_client.get("/login", follow_redirects=True)

    assert b'''Username''' in resp.data
    assert b'''Password''' in resp.data


@patch('flaskr.pages.current_user')
def test_login_get__logged_in(current_userMock, anon_client):
    current_userMock.is_authenticated.return_value = True

    resp = anon_client.get("/login", follow_redirects=True)

    assert b'''Hello fellow sussy bakas!''' in resp.data


@patch("flaskr.pages.backend")
def test_login_post__succes(backendMock, anon_client):
    backendMock.sign_in.return_value = True

    resp = anon_client.post("/login", follow_redirects=True)

    assert b'''Hello fellow sussy bakas!''' in resp.data


@patch("flaskr.pages.backend")
def test_login_post__fail(backendMock, anon_client):
    backendMock.sign_in.return_value = False

    resp = anon_client.post("/login", follow_redirects=True)

    assert b'''User or password is not correct''' in resp.data


def test_logout_get__logged_in(anon_client):
    with anon_client:  # should be logged in as 'cool beanz'
        resp1 = anon_client.post("/login",
                                 data=dict(username='testtest',
                                           password='testtest'),
                                 follow_redirects=True)

        assert b'''Hello there testtest!''' in resp1.data

        resp = anon_client.get("/logout", follow_redirects=True)
        # assert resp.status_code == 200
        assert b'''Username''' in resp.data
        assert b'''Password''' in resp.data


def test_logout_get__logged_out(anon_client):
    resp = anon_client.get("/logout", follow_redirects=True)
    assert b'''Please log in to access this page''' in resp.data
