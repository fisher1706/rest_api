import requests

url = 'http://127.0.0.1:5000/tutorials'

if __name__ == '__main__':
    resp = requests.get(url=url)
    print(resp.json())

    json = {'title': 'Video #4',
            'description': 'Unit test'}

    resp = requests.post(url=url, json=json)
    print(resp.json())

    resp = requests.get(url=url)
    print(resp.json())

    resp = requests.put(url=f'{url}/2', json={'description': 'PUT routes for editing'})
    print(resp)

    resp = requests.get(url=url)
    print(resp.json())

    resp = requests.delete(url=f'{url}/1')
    print(resp)

    resp = requests.get(url=url)
    print(resp.json())
