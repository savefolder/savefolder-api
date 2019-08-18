from core.router import Router
from sanic import Sanic
from settings import *
import views

app = Sanic()  # TODO: Custom wrapper
router = Router(app)
router.register(views)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
