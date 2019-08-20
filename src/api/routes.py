import sanic
from api import views


def setup_routes(app: sanic.Sanic, prefix: str = '') -> None:
    prefix = prefix.rstrip('/')
    views.setup_routes(app, prefix=f'{prefix}/v1')
