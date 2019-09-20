from .settings import settings
import aioredis
import asyncio
import re


class Limiter:
    """
    Convenient anything-per-second limiter
    """

    PERIODS = {
        'sec': 1,
        'second': 1,
        'min': 60,
        'minute': 60,
        'hour': 60 * 60,
        'day': 24 * 60 * 60,
    }
    PATTERN = re.compile(r'(\d+)\s*(?:per|/)\s*(\d+)?\s*(%s)' % '|'.join(PERIODS))

    # Initialized in `get_redis`
    default_redis = None

    def __init__(self, *limits, prefix='', redis=None):
        self.prefix = str(prefix)
        self.limits = [self.parse(i) for i in limits]
        self.limits.sort(key=lambda x: x[1])
        self.redis = redis or self.get_redis()

    @classmethod
    def get_redis(cls):
        if cls.default_redis is None:
            loop = asyncio.get_event_loop()
            future = aioredis.create_redis(settings.REDIS_URL)
            redis = loop.run_until_complete(future)
            cls.default_redis = redis
        return cls.default_redis

    def parse(self, string):
        match = self.PATTERN.match(string)
        if not match: raise SyntaxError('Bad limit string:' + string)
        limit = int(match.group(1))
        number = int(match.group(2) or 1)
        period = self.PERIODS[match.group(3)]
        return limit, number * period

    async def hit(self, key, update=True):
        key = 'limiter:' + self.prefix + ':' + str(key)
        for limit, seconds in self.limits:
            if update: x = await self.redis.incr(key)
            else: x = await self.redis.get(key) or 0
            if update and x == 1: await self.redis.expire(key, seconds)
            elif x > limit: return False
        return True
