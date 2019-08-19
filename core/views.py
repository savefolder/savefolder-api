"""
Custom CBV implementation
"""

from cerberus import Validator
from settings import SECRET
import jwt


class APIError(Exception):
    """
    Custom exception representing API error
    """

    def __init__(self, message, status=500):
        super().__init__(message)
        self.message = message
        self.status = status
        self.response = {
            'status': status,
            'error': message,
        }

    def __repr__(self):
        base = super().__repr__()
        status = 'status=%s' % self.status
        return base[:-1] + ', ' + status + ')'

    def __str__(self):
        base = super().__str__()
        status = '[%s] ' % self.status
        return status + base


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
        cls.validator.allow_unknown = True
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
            return APIError('Internal error', 500).response

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
        raise APIError('Nothing to do', 418)
