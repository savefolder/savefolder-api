import cerberus
import uuid

from . import v1


def add_custom_types() -> None:
    cerberus.Validator.types_mapping['uuid'] = cerberus.TypeDefinition('uuid', (uuid.UUID,), ())


all_schemas = []


def add_schema(name, schema) -> None:
    all_schemas.append(name)
    cerberus.schema_registry.add(name, schema)


def initialize_schemas() -> None:
    add_custom_types()
    add_schema('account.token', v1.ACCOUNT_TOKEN)
    add_schema('account.merge', v1.ACCOUNT_MERGE)
    add_schema('image.upload', v1.IMAGE_UPLOAD)
    add_schema('image.search', v1.IMAGE_SEARCH)


__all__ = [
    'initialize_schemas',
    'all_schemas',
]
