from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/html/', response_class=HTMLResponse, status_code=HTTPStatus.OK)
def read_html():
    return """
    <html>
      <head>
        <title>Nosso ola mundo!</title>
      </head>
      <body>
        <h1> Ola Mundo </h1>
      </body>
    </html>"""


@app.post(
    '/users/',
    response_model=UserPublic,
    status_code=HTTPStatus.CREATED,
)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserList, status_code=HTTPStatus.OK)
def read_users():
    return {'users': database}


@app.get(
    '/users/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK
)
def read_user(user_id: int):
    """
    get a specific user
    """
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return database[user_id - 1]


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
