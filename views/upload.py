from core.settings import settings
from core.views import *
from models import *

from aiohttp import ClientSession, ClientTimeout
from uuid import uuid4
import aioboto3
import aiofiles
import hashlib
import os


# TODO: MOVE TO CORE
class Storage:
    def __init__(self):
        self.client = aioboto3.client(
            service_name='s3',
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )


MAX_SIZE = 1024 * 1024 * 1
CHUNK_SIZE = 1024
TIMEOUT = 1


class UploadImageView(View):
    method = 'images.upload'
    access = Token.USER
    limiting = ['500 / day']
    schema = {
        'url': {'type': 'string', 'required': True, 'url': True},
        'rid': {'type': 'string', 'required': True},
        'tags': {'type': 'string'},
    }
    storage = Storage()

    async def save_to_temp(self):
        success = True
        filename = 'temp/%s.jpg' % uuid4()
        async with aiofiles.open(filename, 'wb') as file:
            async with ClientSession(timeout=ClientTimeout(TIMEOUT)) as client:
                response = await client.get(
                    self.data['url'], chunked=True, read_until_eof=False
                )
                size = 0
                async for chunk in response.content.iter_chunked(CHUNK_SIZE):
                    size += len(chunk)
                    if size > MAX_SIZE:
                        success = False
                        break
                    await file.write(chunk)

        if not success:
            os.remove(filename)
            return None

        return filename

    async def process(self):
        file = await self.save_to_temp()
        if file is None:
            raise APIError('Download error', 400)
        print(file)
        return {'ok': True}
