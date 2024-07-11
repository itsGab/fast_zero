from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_get_token_exception_incorrect_email(client, user):
    response = client.post(
        'auth/token',
        data={'username': 'incorrect-email', 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert token == {'detail': 'Incorrect email or password'}


def test_get_token_exception_incorrect_password(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': 'incorrect-password'},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert token == {'detail': 'Incorrect email or password'}
