from http import HTTPStatus

from fastapi_zero.schemas import UserPublicSchema


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
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'password': 'senha',
            'username': 'username',
            'email': '123@teste.com',
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


def test_user_delete(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Foi jogar no Vasco'}


def test_user_delete_error(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_user_with_id(client, user):
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
