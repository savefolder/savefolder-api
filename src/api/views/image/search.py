import logging

from sanic import views, response, request

from api import security


LOGGER = logging.getLogger('api.views.image.search')


class Search(views.HTTPMethodView):
    permission_decorators = [
        security.json_content_type_perm(),
        security.service_token_perm,
        security.user_token_perm,
    ]
    authentication_decorators = [
        security.service_token_auth,
        security.user_token_auth,
    ]

    decorators = permission_decorators + authentication_decorators

    @staticmethod
    @security.validate_schema('image.search')
    async def post(request: request.Request) -> response.HTTPResponse:
        app = request.app
        return response.json()
