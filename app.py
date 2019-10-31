from core.settings import settings
from core.router import Router
from sanic import Sanic
import asyncio
import views

app = Sanic()  # TODO: Custom wrapper
loop = asyncio.get_event_loop()
router = Router(app, prefix='v0')
router.register(views)

if __name__ == '__main__':
    serve = app.create_server(
        host=settings.HOST,
        port=settings.PORT,
        return_asyncio_server=True,
    )
    asyncio.ensure_future(serve, loop=loop)
    loop.run_forever()
