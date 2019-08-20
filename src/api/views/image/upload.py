import base64
import bson
import io
import logging
import requests
import retrying

from sanic import views, response, request

from api import security


LOGGER = logging.getLogger('api.views.image.upload')


class ID(views.HTTPMethodView):
    permission_decorators = [
        security.service_token_perm,
        security.user_token_perm,
    ]
    authentication_decorators = [
        security.service_token_auth,
        security.user_token_auth,
    ]

    decorators = permission_decorators + authentication_decorators

    @staticmethod
    @security.validate_schema('image.upload')
    async def post(request: request.Request) -> response.HTTPResponse:
        user_id = request['user'].id
        users = request.app.db['users']

        image_id = bson.ObjectId()

        LOGGER.info(
            f'Received image upload request with parameters: content-type={request.content_type}, user_id={user_id}'
        )

        if 'multipart/form-data' in request.content_type.lower():
            image = io.BytesIO(request.files.get('image').body)
        elif 'application/json' in request.content_type.lower():
            data = request.json()
            if 'base64' in data:
                image = io.BytesIO(base64.decodebytes(bytes(data['base64'], 'utf-8')))
            elif 'url' in data:
                @retrying.retry(wait_exponential_multiplier=100, wait_exponential_max=1000)
                def get_image_from_url(url):
                    # todo: do something with synchronous nature of requests library
                    response = requests.get(url, stream=True)
                    response.raise_for_status()
                    return io.BytesIO(response.content)
                image = get_image_from_url(data['url'])
            else:
                image = None
        else:
            image = None

        if image is None:
            return response.json({'error': 'No image data found'}, status=400)

        request.app.storage.upload(f'{user_id}/{image_id}', image)
        await users.update_one({'_id': bson.ObjectId(user_id)}, {'$push': {'images': {'_id': image_id}}})

        return response.json({'image_id': str(image_id)})
