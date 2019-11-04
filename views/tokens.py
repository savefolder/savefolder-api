from core.views import View, APIError
from core.token import Token
from bson import ObjectId
from models import *


class TokensAcquireView(View):
    method = 'tokens.acquire'
    access = Token.SERVICE
    schema = {
        'rid': {'type': 'string', 'required': True},
        'create': {'type': 'boolean', 'default': True},
    }

    async def process(self):
        service = await Service.find_one({'id': ObjectId(self.token.sid)})
        user = await User.find_one({'service': service.id, 'rid': self.data.rid})
        if user: return {'token': user.token, 'created': False}
        if not self.data.create: raise APIError('User not found', 404)

        user = User(service=service, rid=self.data.rid)
        await user.commit()
        user.token = Token.create(uid=user.id, sid=service.id).string
        print(user.token)
        await user.commit()
        return {'token': user.token, 'created': True}


class TokensRefreshView(View):
    method = 'tokens.refresh'
    access = None
    schema = {}

    async def authenticate(self):
        await self.check_token(allow_expired=True, check_access=False)
        if not self.token.expired: raise APIError('Token is not expired yet', 400)

    async def process(self):
        if self.token.is_user():
            id = ObjectId(self.token.uid)
            target = await User.find_one({'id': id})
        elif self.token.is_service():
            id = ObjectId(self.token.sid)
            target = await Service.find_one({'id': id})
        else:
            raise APIError('Unknown token type', 400)

        target.token = Token.create(
            uid=self.token.uid,
            sid=self.token.sid,
            access=self.token.access,
        ).string
        await target.commit()
        return {'token': target.token}
