"""
Custom CBV implementation
"""

from cerberus import Validator
from settings import SECRET
import jwt


class APIError(Exception):
    def __init__(self, message, status):
        super().__init__(message)
        self.status = status
        self.response = {
            'status': status,
            'error': message,
        }


class View:
    method = 'abstract'
    limiting = ['100 / sec']
    service = False
    schema = {}

    def __init__(self, data):
        self.data = data
        self.token = None

    def __init_subclass__(cls):
        cls.validator = Validator(cls.schema)
        # TODO: Build limiter

    @classmethod
    async def handle(cls, data):
        try:
            view = cls(data)
            await view.authenticate()
            await view.validate()
            return await view.process()
        except APIError as exc:
            return exc.response
        except Exception as exc:
            print('Internal error:', exc)  # TODO: Logging
            return {'status': 500, 'error': 'Internal error'}

    async def authenticate(self):
        if 'token' not in self.data:
            raise APIError('Token required', 403)
        token = str(self.data.pop('token'))
        try:
            # TODO: Move to separate class
            data = jwt.decode(token, SECRET, algorithms=['HS256'])
            self.token = data
        except jwt.ExpiredSignatureError:
            raise APIError('Token expired', 403)
        except jwt.InvalidTokenError:
            # TODO: Bad token RPS+IP limiting
            raise APIError('Invalid token', 403)
        if self.token.get('uid') and self.service:
            raise APIError('Access denied', 403)
        # TODO: RPS limiting

    async def validate(self):
        self.data = self.validator.validated(self.data)
        if self.data is None:
            message = str(self.validator.errors)  # TODO
            raise APIError('Validation error: ' + message, 400)

    async def process(self):
        # Should be overridden
        return {'status': 418, 'error': 'Nothing to do'}
