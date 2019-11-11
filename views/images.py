from bson import ObjectId
from core.views import *
from models import *


class BaseImageView(View):
    method = 'images.test'
    access = Token.USER
    schema = {
        'id': {'type': 'string', 'coerce': ObjectId},
        'rid': {'type': 'string'},
    }

    async def validate(self):
        await super().validate()
        print('>>>', self.data)
        if not self.data.get('id') and not self.data.get('rid'):
            error = APIError('Validation error', 400)
            message = {'*': ['Either \'id\' or \'rid\' field must be provided']}
            error.response['details'] = message
            raise error

    async def get_image(self):
        if self.data.get('id'):
            return await Image.find_one({'id': self.data['id']})
        if self.data.get('rid'):
            return await Image.find_one({'rid': self.data['rid']})


class UpdateImageView(BaseImageView):
    method = 'images.update'
    schema = {
        **BaseImageView.schema,
        'tags': {'type': 'string'},
    }


class GetImageView(View):
    method = 'images.get'


class DeleteImageView(View):
    method = 'images.delete'
