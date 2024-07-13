from http import HTTPStatus

import pytest
from fastapi.exceptions import HTTPException
from jwt import decode

from fast_zero.security import create_access_token, get_current_user, settings


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']  # test if 'exp' value was added to token


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid-token'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_exception_decode_error(session):
    # test case for JWT token error (or decode error)
    with pytest.raises(HTTPException):
        get_current_user(session, token='invalid-token')


def test_get_current_user_exception_user_is_none(session):
    # test case for user not found in the database
    data_no_username = {'sub': 'test@test'}
    token = create_access_token(data_no_username)

    with pytest.raises(HTTPException):
        get_current_user(session, token)


def test_get_current_user_exception_no_username(session):
    # test case for missing 'sub' in the payload
    data_user_none = {'test': 'test'}
    token = create_access_token(data_user_none)

    with pytest.raises(HTTPException):
        get_current_user(session, token)
