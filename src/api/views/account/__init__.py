import sanic

from .token import Token
from .merge import Merge


def setup_routes(app: sanic.Sanic, prefix: str = '') -> None:
    prefix = prefix.rstrip('/')
    app.add_route(Token.as_view(), f'{prefix}/token')
    app.add_route(Merge.as_view(), f'{prefix}/merge')
