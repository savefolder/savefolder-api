import functools
import logging
import typing

from authlib.jose import jwt, errors
from sanic import request, response

from api import app


LOGGER = logging.getLogger('api.security.user')


class User:
    def __init__(self, token: str = None):
        self.token = token
        try:
            decoded_data = jwt.decode(token or '', app.config['auth']['key'])
            self.id = decoded_data['_id']
        except (errors.BadSignatureError, errors.DecodeError) as e:
            LOGGER.warning(f'Failed to decode JWT: {repr(e)}')
            self.id = None

    def is_authenticated(self):
        return self.id is not None


def user_token_auth(function: typing.Callable) -> typing.Callable:
    @functools.wraps(function)
    def wrapper(request: request.Request, *args, **kwargs) -> response.HTTPResponse:
        user_token = request.headers.get('User-Token')
        request['user'] = User(user_token)
        return function(request, *args, **kwargs)
    return wrapper


def user_token_perm(function: typing.Callable) -> typing.Callable:
    @functools.wraps(function)
    async def wrapper(request: request.Request, *args, **kwargs) -> response.HTTPResponse:
        if 'user' in request and request['user'].is_authenticated():
            return await function(request, *args, **kwargs)
        LOGGER.warning(f'Request with invalid user token: {request.get("user")}')
        return response.json({'error': 'Invalid user token'}, status=403)
    return wrapper


__all__ = [
    'user_token_auth',
    'user_token_perm',
]
