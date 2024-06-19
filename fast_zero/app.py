from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message

app = FastAPI()


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
