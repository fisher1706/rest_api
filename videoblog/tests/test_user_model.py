def test_model(user):
    assert user.name == 'TestUser'


def test_user_login(user, client):
    resp = client.post('/login', json={
        'email': user.email,
        'password': 'password'
    })

    assert resp.status_code == 200
    assert resp.get_json().get('access_token')


def test_user_reg(client):
    resp = client.post('/register', json={
        'name': 'TestUser',
        'email': 'test@test.com',
        'password': 'password'
    })

    assert resp.status_code == 200
