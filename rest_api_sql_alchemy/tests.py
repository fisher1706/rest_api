from random import random
from .app import client
from .models import Video


url = 'http://127.0.0.1:5000/tutorials'


def test_get():
    resp = client.get(url)
    print(f'\nresponse: {resp.get_json()}')

    assert resp.status_code == 200


def test_post():
    number = int(random() * 1000000)

    data = {
        'name': f'Unit Tests #{number}',
        'description': f'Pytest tuttorial # {number}'
    }

    resp = client.post(url, json=data)
    print(f'\nresponse: {resp.get_json()}')

    assert resp.status_code == 200
    assert resp.get_json()['name'] == data['name']


def test_put():
    video_id = Video.query.all()[-1].id
    resp = client.put(f'{url}/{video_id}', json={'description': 'zapel'})

    assert resp.status_code == 200
    assert Video.query.get(video_id).description == 'zapel'


def test_delete():
    video_id = Video.query.all()[-1].id
    resp = client.delete(f'{url}/{video_id}')

    assert resp.status_code == 204
    assert Video.query.get(video_id) is None
