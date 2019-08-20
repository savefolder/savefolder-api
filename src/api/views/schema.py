import cerberus

from sanic import views, request, response, exceptions
from api.schemas import all_schemas


class Schema(views.HTTPMethodView):
    async def get(self, _: request.Request, name: str) -> response.HTTPResponse:
        if name == '__all__':
            schemas = {}
            for schema in all_schemas:
                schemas[schema] = cerberus.schema_registry.get(schema)
            return response.json(schemas)
        schema = cerberus.schema_registry.get(name)
        if schema is None:
            raise exceptions.NotFound('Schema not found')
        return response.json(schema)
