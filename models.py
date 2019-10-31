from core.models import Model, fields

__all__ = [
    'Service',
    'User',
    'Image',
]


class Service(Model):
    name = fields.StringField()


class User(Model):
    service = fields.ReferenceField(Service)


class Image(Model):
    owner = fields.ReferenceField(User)
    tags = fields.StringField()
    url = fields.URLField()
    rids = fields.DictField()
