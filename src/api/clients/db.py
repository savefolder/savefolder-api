from motor import motor_asyncio

from api import settings
from common import Singleton


class Database(metaclass=Singleton):
    def __init__(self, loop=None, *args, **kwargs):
        self.client = motor_asyncio.AsyncIOMotorClient(
            host=settings.mongo_config['host'],
            port=settings.mongo_config['port'],
            username=settings.mongo_config.get('username'),
            password=settings.mongo_config.get('password'),
            io_loop=loop,
        )
        self.db = self.client[settings.mongo_config['database']]

    def setup_indexes(self) -> None:
        self.db.merge.create_index('key', unique=True)
