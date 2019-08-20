import sanic

from . import account, schema, image


def setup_routes(app: sanic.Sanic, prefix: str = '') -> None:
    prefix = prefix.rstrip('/')
    app.add_route(schema.Schema.as_view(), f'{prefix}/schema/<name:string>')
    account.setup_routes(app, prefix=f'{prefix}/account')
    image.setup_routes(app, prefix=f'{prefix}/image')
