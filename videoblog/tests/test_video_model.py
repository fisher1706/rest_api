def test_list(user, video, client, user_headers):
    resp = client.get('/tutorials', headers=user_headers)
    print(f'\nresp: {resp.get_json()}')

    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


def test_new_video(user, client, user_headers):
    resp = client.post('/tutorials', json={
        'description': 'Description#1',
        'name': 'Video#1'
    }, headers=user_headers)
    print(f'\nresp: {resp.get_json()}')

    assert resp.status_code == 200


def test_edit_video(video, client, user_headers):
    resp = client.put(f'/tutorials/{video.id}', json={
        'description': 'Description#1_upd',
        'name': 'Video#1_upd'
    }, headers=user_headers)
    print(f'\nresp: {resp.get_json()}')

    assert resp.status_code == 200


def test_delete_video(video, client, user_headers):
    resp = client.delete(f'/tutorials/{video.id}', json={
        'description': 'Description#1_upd',
        'name': 'Video#1_upd'
    }, headers=user_headers)

    assert resp.status_code == 204

