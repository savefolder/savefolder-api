import cerberus
import functools
import logging
import typing

from sanic import request, response


LOGGER = logging.getLogger('api.security.schema')


def validate_schema(schema: typing.Union[str, dict]) -> typing.Callable:
    def validate(function: typing.Callable) -> typing.Callable:
        @functools.wraps(function)
        async def wrapper(request: request.Request, *args, **kwargs) -> response.HTTPResponse:
            if isinstance(schema, str):
                validator = cerberus.Validator(cerberus.schema_registry.get(schema))
            else:
                validator = cerberus.Validator(schema)
            if validator.validate(request.json):
                return await function(request, *args, **kwargs)
            LOGGER.warning(f'Request with incorrect schema: {validator.errors}')
            return response.json({'error': f'Schema Validation Error: {validator.errors}'}, status=400)
        return wrapper
    return validate


def validate_schema_if_json_content_type(schema: typing.Union[str, dict]) -> typing.Callable:
    def validate(function: typing.Callable) -> typing.Callable:
        @functools.wraps(function)
        async def wrapper(request: request.Request, *args, **kwargs) -> response.HTTPResponse:
            if isinstance(schema, str):
                validator = cerberus.Validator(cerberus.schema_registry.get(schema))
            else:
                validator = cerberus.Validator(schema)
            if 'application/json' not in request.content_type or validator.validate(request.json):
                return await function(request, *args, **kwargs)
            LOGGER.warning(f'Request with incorrect schema: {validator.errors}')
            return response.json({'error': f'Schema Validation Error: {validator.errors}'}, status=400)
        return wrapper
    return validate
