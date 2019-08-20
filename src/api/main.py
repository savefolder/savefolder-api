import logging
import sanic

from asyncio import events

from api import settings


app = sanic.Sanic(configure_logging=False)
app.config.update(settings.app_config)


@app.listener('before_server_start')
async def before_server_start(app: sanic.Sanic, loop: events.AbstractEventLoop) -> None:
    from api import schemas, routes, clients

    logging.basicConfig(**settings.logging_config)

    database = clients.Database(loop)
    database.setup_indexes()

    # setup database
    app.db = database.db

    # setup storage
    app.storage = clients.Storage()

    # initialize schemas
    schemas.initialize_schemas()

    # setup routes
    routes.setup_routes(app)


if __name__ == '__main__':
    # ssl_paths = {
    #     'cert': f'{str(BASE_DIR).rstrip("/")}/.ssl/certificate.crt',
    #     'key': f'{str(BASE_DIR).rstrip("/")}/.ssl/keyfile.key',
    # }
    # app.go_fast('0.0.0.0', 8080, ssl=ssl_paths, auto_reload=True)
    app.go_fast('0.0.0.0', 8080, auto_reload=True, debug=True)
