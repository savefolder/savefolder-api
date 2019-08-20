import boto3
import io
import sanic.request
import typing

from api import settings
from common import Singleton


class Storage(metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        self.bucket = settings.storage_config['bucket']
        self.session = boto3.session.Session()
        self.client = self.session.client(
            service_name=settings.storage_config['service_name'],
            endpoint_url=settings.storage_config['endpoint_url'],
            aws_access_key_id=settings.storage_config['aws_access_key_id'],
            aws_secret_access_key=settings.storage_config['aws_secret_access_key'],
        )

    def upload(self, key: str, file: typing.Union[sanic.request.File, bytes, io.BytesIO]) -> None:
        self.client.upload_fileobj(file, self.bucket, key)

    def get_download_url(self, key, expires_in=300):
        return self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket, 'Key': key},
            ExpiresIn=expires_in,
        )
