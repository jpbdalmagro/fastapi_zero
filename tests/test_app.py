from http import HTTPStatus


def test_root_deve_retornar_ola_mundo(client):

    response = client.get('/')
    assert response.json() == {'message': 'Olá mundo'}
    assert response.status_code == HTTPStatus.OK


def test_exercicio_ola_mundo_em_html(client):

    response = client.get('/exercicio-html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text


def test_user_register(client):

    response = client.post(
        'users',
        json={
            'username': 'alice',
            'email': 'alice@teste.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@teste.com',
        'username': 'alice',
    }


def test_users_list(client):

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'email': 'alice@teste.com',
                'username': 'alice',
            },
        ]
    }


def test_update(client):

    response = client.put(
        '/users/1',
        json={
            'username': 'carlos',
            'email': 'carlos@teste.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'carlos',
        'email': 'carlos@teste.com',
        'id': 1,
    }


def test_get_user_should_return_not_found__exercicio(client):
    response = client.get('/users/666')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_user___exercicio(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'carlos',
        'email': 'carlos@teste.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_not_found_updadte(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'carlos',
            'email': 'carlos@teste.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_not_found_delete(client):
    response = client.delete('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
