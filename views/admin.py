from core.views import *
from models import *


class CreateServiceView(View):
    method = 'services.create'
    access = Token.ADMIN
    schema = {
        'name': {'type': 'string', 'required': True, 'empty': False}
    }

    async def process(self):
        service = Service(name=self.data['name'])
        await service.commit()
        service.token = Token.create(sid=service.id).string
        await service.commit()
        return service.dump()
