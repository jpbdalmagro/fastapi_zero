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


def test_update_user_error(client):
    response = client.put(
        '/users/2',
        json={
            'password': 'senha',
            'username': 'username',
            'email': '123@teste.com',
            'id': 2,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_user_with_id(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'username',
        'email': '123@teste.com',
        'id': 1,
    }


def test_get_user_with_id_error(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_delete(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Foi jogar no Vasco'}


def test_user_delete_error(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
