from core.settings import settings
from core.router import Router
from aiohttp import web
import views

app = web.Application()
router = Router(app, prefix='v0')
router.register(views)


async def status(_):
    return web.json_response({
        'status': 200,
        'ok': True,
    })


if __name__ == '__main__':
    app.router.add_route('*', '/', status)
    web.run_app(
        app,
        host=settings.HOST,
        port=settings.PORT,
    )
