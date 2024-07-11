from http import HTTPStatus

# `TestClient` and `app` replace by `client` stored in conftest.py
# from fastapi.testclient import TestClient
# from fast_zero.app import app


def test_read_root_should_return_hello_world(client):
    # client = TestClient(app)  # arrange -> replace by fixture

    response = client.get('/')  # act

    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {'message': 'Hello World!'}


def test_read_root_should_return_html_hello_world(client):
    response = client.get('/html/')

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
    <html>
      <head>
        <title> Our Hello World! </title>
      </head>
      <body>
        <h1> Hello World! </h1>
      </body>
    </html>"""
    )
