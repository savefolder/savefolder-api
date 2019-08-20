import functools
import logging
import typing

from sanic import request, response

from api.settings import services_config


LOGGER = logging.getLogger('api.security.service')


class Service:
    token_mapping = {token: service for service, token in services_config.items()}

    def __init__(self, token: str = None):
        self.token = token
        self.id = Service.token_mapping.get(token)

    def is_authenticated(self):
        return self.id is not None

    def __str__(self):
        return str(self.id)


def service_token_auth(function: typing.Callable) -> typing.Callable:
    @functools.wraps(function)
    async def wrapper(request: request.Request, *args, **kwargs) -> response.HTTPResponse:
        service_token = request.headers.get('Service-Token')
        request['service'] = Service(service_token)
        return await function(request, *args, **kwargs)
    return wrapper


def service_token_perm(function: typing.Callable) -> typing.Callable:
    @functools.wraps(function)
    async def wrapper(request: request.Request, *args, **kwargs) -> response.HTTPResponse:
        if 'service' in request and request['service'].is_authenticated():
            return await function(request, *args, **kwargs)
        LOGGER.warning(f'Request with invalid service token: {request.get("service")}')
        return response.json({'error': 'Invalid service token'}, status=403)
    return wrapper


__all__ = [
    'service_token_auth',
    'service_token_perm',
]
