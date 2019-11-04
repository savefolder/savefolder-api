from umongo import Instance, Document, fields, validate
from motor.motor_asyncio import AsyncIOMotorClient
from .settings import settings

__all__ = [
    'fields',
    'validate',
    'register',
    'Model',
]

motor = AsyncIOMotorClient(settings.MONGO_URL)
register = Instance(motor.main).register


def pluralize(word):
    if word[-1] in ('s', 'x', 'z'): return word + 'es'
    if word[-2:] in ('ss', 'sh', 'ch'): return word + 'es'
    return word + 's'


@register
class Model(Document):
    """
    Base model class extending umongo's `Document`
    """

    class Meta:
        abstract = True

    def __init_subclass__(cls):
        if cls.Meta != Model.Meta: return
        collection = pluralize(cls.__name__.lower())
        cls.Meta = type('Meta', (), {'collection_name': collection})
