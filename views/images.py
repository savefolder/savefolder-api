from core.views import *


class UploadImageView(View):
    method = 'images.upload'
    access = Token.USER
    limiting = ['500 / day']
    schema = {
        'url': {'type': 'url', 'required': True},
        'rid': {'type': 'string'},
        'tags': {'type': 'string'},
    }

    async def process(self):
        pass


class BaseImageReferenceView(View):
    method = 'images.test'
    access = Token.USER
    schema = {
        'id': {'type': 'string'},
        'rid': {'type': 'string'},
    }

    async def validate(self):
        await super().validate()
        if 'id' not in self.data and 'rid' not in self.data:
            error = APIError('Validation error', 400)
            message = 'Either \'id\' or \'rid\' field must be provided'
            error.response['details'] = message
            raise error

    async def get_image(self):
        pass


class UpdateImageView(View):
    method = 'images.update'
    access = Token.USER
    schema = {
        'tags': {'type': 'string'},
    }


class GetImageView(View):
    method = 'images.get'
    access = Token.USER
    schema = {
        'url': {'type': 'url', 'required': True},
        'rid': {'type': 'string'},
        'tags': {'type': 'string'},
    }


class DeleteImageView(View):
    method = 'images.delete'
    access = Token.USER
