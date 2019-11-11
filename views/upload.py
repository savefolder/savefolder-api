from core.settings import settings
from core.views import *
from models import *

from aiohttp import ClientSession, ClientTimeout
from uuid import uuid4
import aioboto3
import aiofiles
import warnings
import asyncio
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
MAX_PX_SIZE = 6000 * 6000
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

    async def download(self, filename):
        """
        Downloads data from remote URL to provided file
        Raises error if file size exceeds limit
        (!) Does not delete file in case of error
        In case of success, returns computed MD5 hash
        """
        async with aiofiles.open(filename, 'wb') as file:
            async with ClientSession(timeout=ClientTimeout(TIMEOUT)) as client:
                response = await client.get(self.data['url'], read_until_eof=False)
                md5 = hashlib.md5()
                size = 0
                async for chunk in response.content.iter_chunked(CHUNK_SIZE):
                    md5.update(chunk)
                    size += len(chunk)
                    if size > MAX_SIZE:
                        raise APIError('Too large file', 400)
                    await file.write(chunk)
        return md5

    @staticmethod
    def check(filename):
        """
        Checks if file is valid image and it's not too big
        This method is static because it's supposed to run
        in separate executor, not main event loop
        """
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('error')
                im = Image.open(filename)
            pixels = im.size[0] * im.size[1]
            if pixels > MAX_PX_SIZE:
                return APIError('Too large image', 400)
        except Image.DecompressionBombWarning:
            return APIError('Decompression bomb error', 400)
        except IOError:
            return APIError('Bad image file', 400)

    async def process(self):
        try:
            filename = str(uuid4())
            md5 = await self.download(filename)
            # TODO: RUN IN EXECUTOR
            error = self.check(filename)
            if isinstance(error, APIError):
                raise error
        finally:
            if os.path.isfile(filename):
                os.remove(filename)
