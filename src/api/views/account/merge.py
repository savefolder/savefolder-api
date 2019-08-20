import datetime
import logging
import random

from pymongo import errors
from sanic import request, response, views

from api import security


LOGGER = logging.getLogger('api.views.account.token')


class Merge(views.HTTPMethodView):
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

    KEY_RECREATION_MAX_ATTEMPTS = 5

    @staticmethod
    @security.validate_schema(schema='account.merge')
    async def post(request: request.Request) -> response.HTTPResponse:
        app = request.app

        service = request['service']
        user = request['user']

        LOGGER.info(f'Received merge request from service {service} for user {user["id"]}')

        merge = app.db['merge']
        service_users = app.db[str(service)]

        result = await service_users.find_one({'user_id': user['id']})
        if result is None:
            return response.json({'error': 'Account not found'}, status=400)
        user_id = result['user_id']

        recreate_key = request.json.get('recreate_key')
        key = request.json.get('key')
        if key is None:
            LOGGER.info('Key is not in request')
            result = await merge.find_one({'_id': user_id})
            if result is not None:
                now = datetime.datetime.utcnow()
                if result['start'] + result['duration'] < now or recreate_key:
                    await merge.delete_one(result)
                else:
                    LOGGER.info(f'Returning existing merge doc: {result}')
                    return response.json({
                        'start': result['start'],
                        'duration': result['duration'],
                        'key': result['key'],
                    })

            start = datetime.datetime.utcnow()
            duration = datetime.timedelta(seconds=app.config['merge']['duration']).total_seconds()
            key = random.randint(*app.config['merge']['key_range'])
            merge_doc = {
                '_id': result['user_id'],
                'start': start,
                'duration': duration,
                'key': key,
            }

            for i in range(Merge.KEY_RECREATION_MAX_ATTEMPTS):
                try:
                    await merge.insert_one(merge_doc)
                    break
                except errors.DuplicateKeyError:
                    LOGGER.warning(f'DuplicateKeyError for key {key}, attempt {i}')
                    if i + 1 == Merge.KEY_RECREATION_MAX_ATTEMPTS:
                        LOGGER.error(f'Failed to create merge key after {Merge.KEY_RECREATION_MAX_ATTEMPTS} attempts')
                        return response.HTTPResponse(status=500)

            LOGGER.info(f'Returning created merge doc: {merge_doc}')
            return response.json({
                'start': start.isoformat(),
                'duration': duration,
                'key': key,
            })

        result = await merge.find_one(user_id)
        if result is None:
            LOGGER.info(f'Merge was not initiated for key: {key}')
            return response.json({'error': 'Merge was not initiated'}, status=400)

        stored_key = result['key']
        LOGGER.info(f'Stored key: {stored_key}, request key: {key}')
        if stored_key != key:
            return response.json({'error': 'Incorrect merge key'}, status=400)

        token = 123

        return response.json({'token': token})
