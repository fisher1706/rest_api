from .app import client
from random import random


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
    assert resp.get_json()[-1]['name'] == data['name']


def test_put():
    resp = client.put(f'{url}/1', json={'name': 'zapel'},)
    print(f'\nresponse: {resp.get_json()}')

    assert resp.status_code == 200


def test_delete():
    resp = client.delete(f'{url}/1')

    assert resp.status_code == 204
