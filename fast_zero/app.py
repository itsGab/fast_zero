from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message

app = FastAPI()
# routers imported in the `fast_zero.__init__.py`

tag_root = 'basic'


@app.get(
    '/', response_model=Message, status_code=HTTPStatus.OK, tags=[tag_root]
)
def read_root():
    return {'message': 'Hello World!'}


@app.get(
    '/html/',
    response_class=HTMLResponse,
    status_code=HTTPStatus.OK,
    tags=[tag_root],
)
def read_html():
    return """
    <html>
      <head>
        <title> Our Hello World! </title>
      </head>
      <body>
        <h1> Hello World! </h1>
      </body>
    </html>"""
