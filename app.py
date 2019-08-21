from core.router import Router
from core import settings
from sanic import Sanic
import views

app = Sanic()  # TODO: Custom wrapper
router = Router(app)
router.register(views)

if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)
