import bson
import logging

from datetime import datetime
from sanic import views, response, request

from api import security


LOGGER = logging.getLogger('api.views.image.download_url')


class DownloadURL(views.HTTPMethodView):
    DEFAULT_URL_EXPIRATION_TIME = 300
    MAX_URL_EXPIRATION_TIME = 3600

    permission_decorators = [
        security.service_token_perm,
        security.user_token_perm,
    ]
    authentication_decorators = [
        security.service_token_auth,
        security.user_token_auth,
    ]

    decorators = permission_decorators + authentication_decorators

    async def get(self, request: request.Request, image_id: str) -> response.HTTPResponse:
        app = request.app
        user_id = request['user'].id

        LOGGER.info(f'Received download url request for image id: {image_id}, from user: {user_id}')

        result = await app.db.users.find_one(
            {'_id': bson.ObjectId(user_id), 'images': {'_id': bson.ObjectId(image_id)}},
            {'_id': 1},
        )
        if result is None:
            return response.json({'error': 'Unknown image id'}, status=400)

        try:
            expires_in = min(
                int(request.args.get('expires_in', DownloadURL.DEFAULT_URL_EXPIRATION_TIME)),
                DownloadURL.DEFAULT_URL_EXPIRATION_TIME,
            )
        except (ValueError, IndexError):
            expires_in = DownloadURL.DEFAULT_URL_EXPIRATION_TIME

        LOGGER.info(f'Creating download url which will expire in {expires_in} seconds')

        timestamp = int(datetime.timestamp(datetime.utcnow())) + expires_in
        storage_id = f'{user_id}/{image_id}'
        url = app.storage.get_download_url(storage_id, expires_in)

        return response.json({'url': url, 'expires': timestamp})
