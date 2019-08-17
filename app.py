from core.router import Router
from sanic import Sanic
from settings import *

app = Sanic()  # TODO: Custom wrapper
router = Router(app)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
