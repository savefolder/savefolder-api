import logging

from authlib.jose import jwt
from sanic import views, response, request

from api import security


LOGGER = logging.getLogger('api.views.account.token')


class Token(views.HTTPMethodView):
    permission_decorators = [
        security.json_content_type_perm(),
        security.service_token_perm,
    ]
    authentication_decorators = [
        security.service_token_auth,
    ]

    decorators = permission_decorators + authentication_decorators

    @staticmethod
    @security.validate_schema(schema='account.token')
    async def post(request: request.Request) -> response.HTTPResponse:
        app = request.app

        service = request['service']
        user_id = request.json['id']
        LOGGER.info(f'Received token request for service "{service}" with id "{user_id}"')

        users = app.db['users']
        service_users = app.db[str(service)]
        user = await service_users.find_one({'user_id': user_id})
        if user is None:
            result = await users.insert_one({})

            LOGGER.info(f'Created new user with id: {result.inserted_id}')

            header = {'alg': app.config['auth']['alg']}
            payload = {'service': str(service), '_id': str(result.inserted_id)}
            key = app.config['auth']['key']
            token = jwt.encode(header, payload, key)

            await service_users.insert_one({
                '_id': result.inserted_id,
                'user_id': user_id,
                'token': token,
            })
            created = True
        else:
            token = user['token']
            created = False

        return response.json({
            'token': token,
            'created': created,
        })
