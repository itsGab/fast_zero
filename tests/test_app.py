from http import HTTPStatus

from fast_zero.schemas import UserPublic

# `TestCliente` e `app` trocado por `client` no conftest.py
# from fastapi.testclient import TestClient

# from fast_zero.app import app


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    # client = TestClient(app)  # arrange -> substituido por fixture

    response = client.get('/')  # act

    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {'message': 'Olá Mundo!'}


def test_read_html_deve_retorno_ok_e_html_ola_mundo(client):
    response = client.get('/html/')

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
    <html>
      <head>
        <title>Nosso ola mundo!</title>
      </head>
      <body>
        <h1> Ola Mundo </h1>
      </body>
    </html>"""
    )


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'username',
            'email': 'username@email.com',
            'password': 'password123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'username',
        'email': 'username@email.com',
    }


def test_create_user_exception_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'username@email.com',
            'password': 'password123',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_exception_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'username',
            'email': 'teste@mail.com',
            'password': 'password123',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'E-mail already exists'}


def test_read_users_empty(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_exception(client):
    response = client.get('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'updated',
            'email': 'updated@email.com',
            'password': 'newsecret',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'updated',
        'email': 'updated@email.com',
        'id': 1,
    }


def test_update_user_exception(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'updated_username',
            'email': 'updated@email.com',
            'password': 'thisissecret',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}

    response = client.put(
        '/users/0',
        json={
            'username': 'updated_username',
            'email': 'updated@email.com',
            'password': 'thisissecret',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_exception(client):
    response = client.delete('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
