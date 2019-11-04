from core.models import *

__all__ = [
    'Service',
    'User',
    'Image',
]


@register
class Service(Model):
    token = fields.StringField()
    name = fields.StringField()


@register
class User(Model):
    token = fields.StringField()
    service = fields.ReferenceField(Service)
    rid = fields.StringField()


@register
class Image(Model):
    owner = fields.ReferenceField(User)
    tags = fields.StringField()
    url = fields.URLField()
    rids = fields.DictField()
