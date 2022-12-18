import pytest
import sys

sys.path.append('..')

from videoblog import app, Base, engine, session as db_session
from videoblog.models import User, Video


@pytest.yield_fixture()
def testapp():
    _app = app
    Base.metadata.create_all(bind=engine)
    _app.connection = engine.connect()

    yield app

    Base.metadata.drop_all(bind=engine)
    _app.connection.close()


@pytest.fixture()
def session(testapp):
    ctx = app.app_context()
    ctx.push()

    yield db_session

    db_session.close_all()
    ctx.pop()


@pytest.fixture()
def user(session):
    user = User(
        name='TestUser',
        email='test@test.com',
        password='password'
    )

    session.add(user)
    session.commit()

    return user


@pytest.fixture()
def client(testapp):
    return testapp.test_client()


@pytest.fixture()
def user_token(user, client):
    resp = client.post('/login', json={
        'email': user.email,
        'password': 'password'
    })

    return resp.get_json()['access_token']


@pytest.fixture()
def user_headers(user_token):
    headers = {
        'Authorization': f'Bearer {user_token}'
    }

    return headers


@pytest.fixture()
def video(user, session):
    video = Video(
        user_id=user.id,
        name='Video#1',
        description='Description#1'
    )

    session.add(video)
    session.commit()

    return video
