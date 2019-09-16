from core.models import Model, fields


class User(Model):
    # Just an ID placeholder for now
    pass


class Service(Model):
    # Just ad ID placeholder for now
    pass


class Image(Model):
    owner = fields.ReferenceField(User)
    tags = fields.StringField()
    url = fields.URLField()
    rids = fields.DictField()
