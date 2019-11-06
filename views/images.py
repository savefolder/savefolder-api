from core.views import *


class UploadImageView(View):
    method = 'images.upload'
    access = Token.USER
    limiting = ['500 / day']
    schema = {
        'url': {'type': 'string', 'required': True, 'url': True},
        'rid': {'type': 'string', 'required': True},
        'tags': {'type': 'string'},
    }

    async def process(self):
        pass


class BaseImageView(View):
    method = 'images.test'
    access = Token.USER
    schema = {
        'id': {'type': 'string'},
        'rid': {'type': 'string'},
    }

    async def validate(self):
        await super().validate()
        if not self.data.get('id') and not self.data.get('rid'):
            error = APIError('Validation error', 400)
            message = {'*': ['Either \'id\' or \'rid\' field must be provided']}
            error.response['details'] = message
            raise error

    async def get_image(self):
        pass


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
