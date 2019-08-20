from functools import wraps
from sanic import exceptions


def authorize_token(handler):
    @wraps(handler)
    async def wrapper(request, *args, **kwargs):
        from core import app

        token = request.headers.get('Token')
        if token not in app.config.ALLOWED_TOKENS:
            raise exceptions.Unauthorized('Unauthorized')
        return await handler(request, *args, **kwargs)

    return wrapper
