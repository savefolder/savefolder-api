from core.models import *

__all__ = [
    'Service',
    'User',
    'Image',
]


@register
class Service(Model):
    name = fields.StringField()


@register
class User(Model):
    service = fields.ReferenceField(Service)


@register
class Image(Model):
    owner = fields.ReferenceField(User)
    tags = fields.StringField()
    url = fields.URLField()
    rids = fields.DictField()
