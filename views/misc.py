from core.views import View, APIError
from core.token import Token
from models import *


class StatusView(View):
    method = 'status'
    limiting = ['20 / min']

    async def authenticate(self):
        if not await self.limiter.hit('anonymous'):
            raise APIError('Too many requests', 429)

    async def process(self):
        return {'ok': 'ok'}


class TokenView(View):
    method = 'tokens.acquire'
    access = Token.SERVICE
    schema = {
        'rid': {'type': 'string', 'required': True},
        'create': {'type': 'boolean', 'default': True},
    }

    async def process(self):
        # TODO
        user = await User.find_one({'rid': self.data['rid']})
        return user.dump()
