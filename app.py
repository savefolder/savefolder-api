from core.settings import settings
from core.router import Router
from aiohttp import web
import asyncio
import views

app = web.Application()  # TODO: Custom wrapper
loop = asyncio.get_event_loop()
router = Router(app, prefix='v0')
router.register(views)

if __name__ == '__main__':
    web.run_app(
        app,
        host=settings.HOST,
        port=settings.PORT,
    )
