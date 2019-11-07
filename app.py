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


app.router.add_get('/', status)

if __name__ == '__main__':
    web.run_app(
        app,
        host=settings.HOST,
        port=settings.PORT,
    )
