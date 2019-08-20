import logging

from sanic import views, response, request

from api import security


LOGGER = logging.getLogger('api.views.image.tags.get')


class Tags(views.HTTPMethodView):
    permission_decorators = [
        security.service_token_perm,
        security.user_token_perm,
    ]
    authentication_decorators = [
        security.service_token_auth,
        security.user_token_auth,
    ]

    decorators = permission_decorators + authentication_decorators

    async def get(self, request: request.Request) -> response.HTTPResponse:
        app = request.app
        return response.json({})

    async def post(self, request: request.Request) -> response.HTTPResponse:

        return response.json({})

    async def put(self, request: request.Request) -> response.HTTPResponse:
        app = request.app
        return response.json({})

    async def delete(self, request: request.Request) -> response.HTTPResponse:
        app = request.app
        return response.json({})
