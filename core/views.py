"""
Custom CBV implementation
"""

from cerberus import Validator
from .limiter import Limiter
from .token import Token


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
    """
    Base class for all API methods
    """

    method = 'abstract'
    limiting = []
    access = Token.USER
    schema = {}

    def __init__(self, data):
        self.data = data
        self.token = None

    def __init_subclass__(cls):
        cls.validator = Validator(cls.schema)
        cls.validator.allow_unknown = True
        prefix = 'method:' + cls.method
        cls.limiter = Limiter(*cls.limiting, prefix=prefix)

    @classmethod
    async def handle(cls, data):
        try:
            view = cls(data)
            await view.authenticate()
            await view.validate()
            data = await view.process()
            if type(data) == dict: return data
            return {'data': data}
        except APIError as exc:
            return exc.response
        except Exception as exc:
            print('Internal error:', exc)  # TODO: Logging
            return APIError('Internal error', 500).response

    async def authenticate(self):
        if self.access is None: return await self.check_limiting()
        await self.check_token(allow_expired=False, check_access=True)
        key = ''
        if self.token.is_user(): key = self.token.uid
        elif self.token.is_service(): key = self.token.sid
        await self.check_limiting(key=key)

    async def check_limiting(self, key=''):
        if not await self.limiter.hit(key):
            raise APIError('Too many requests', 420)

    async def check_token(self, allow_expired=False, check_access=True):
        if 'token' not in self.data:
            raise APIError('Token required', 403)
        self.token = Token(str(self.data.pop('token')))
        if not self.token.valid:
            raise APIError('Invalid token', 403)
        if not allow_expired and self.token.expired:
            raise APIError('Token expired', 403)
        if check_access and not self.token.check(self.access):
            raise APIError('Access denied', 403)

    async def validate(self):
        self.data = self.validator.validated(self.data)
        if self.data is None:
            error = APIError('Validation error', 400)
            # TODO: Standardize?
            error.response['details'] = self.validator.errors
            raise error

    async def process(self):
        raise APIError('Nothing to do', 418)
