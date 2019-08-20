import functools
import logging
import typing
from sanic import request, response

LOGGER = logging.getLogger('api.security.service')


def content_type_perm(content_type: str) -> typing.Callable:
    def content_type_verifier(function: typing.Callable) -> typing.Callable:
        @functools.wraps(function)
        async def wrapper(request: request.Request, *args, **kwargs) -> response.HTTPResponse:
            if content_type in request.content_type:
                return await function(request, *args, **kwargs)
            LOGGER.warning(f'Request with incorrect content type: {request.content_type}')
            return response.json({'error': 'Incorrect content type'}, status=400)
        return wrapper
    return content_type_verifier


def json_content_type_perm() -> typing.Callable:
    return content_type_perm('application/json')


def form_data_content_type_perm() -> typing.Callable:
    return content_type_perm('multipart/form-data')
