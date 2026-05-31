from http import HTTPStatus


def test_read_root_return_hello_world_and_ok(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'user',
            'email': '123@teste.com',
            'password': 'senhafoda',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'user',
        'email': '123@teste.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'username': 'user', 'email': '123@teste.com'}]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'password': 'senha',
            'username': 'username',
            'email': '123@teste.com',
            'id': 1,
        },
    )

    assert response.json() == {
        'username': 'username',
        'email': '123@teste.com',
        'id': 1,
    }
