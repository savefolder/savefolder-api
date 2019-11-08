from core.settings import settings
from core.router import Router
from aiohttp import web
import views

app = web.Application()
router = Router(app)
router.register(views)


@router.route(path='/')
async def status(_):
    return web.json_response({
        'status': 200,
        'ok': True,
    })


if __name__ == '__main__':
    web.run_app(
        app,
        host=settings.HOST,
        port=settings.PORT,
    )
