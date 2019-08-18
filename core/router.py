"""
Custom mini-router
"""

from sanic.response import HTTPResponse
from core.views import View
import json


class Router:
    """
    Custom mini-router, supporting:
    + Registering package of views
    + Request decoding & encoding
    - Multiple decoding & encoding options
    - URL prefix (may be useful for versioning)
    """

    def __init__(self, app):
        self.app = app
        self.views = {}
        self.app.add_route(
            self.handle,
            '/<path:path>',   # Wildcard path (prefix?)
            ['GET', 'POST'],  # Allow GET & POST only (any?)
        )

    def register(self, package):
        """
        Registers package containing view classes
        Package must declare __all__ variable
        """
        package = package.__dict__
        exports = package['__all__']
        for key in exports:
            cls = package[key]
            if issubclass(cls, View):
                method = cls.method
                self.views[method] = cls

    async def handle(self, request, path=''):
        """
        HTTP request entry point
        """
        # TODO: Allow `method` in data
        method = path.replace('/', '.').strip('.')
        if method not in self.views:
            return self.encode({'status': 404, 'error': 'Unknown method'})
        data = self.decode(request)
        if data is None:
            return self.encode({'status': 400, 'error': 'Bad request'})
        view = self.views[method]
        response = await view.handle(data)
        return self.encode(response)

    def decode(self, request):
        """
        Decodes http request as python dict
        (for now, only json is supported)
        """
        try:
            return request.json
        except:
            return None

    def encode(self, response):
        """
        Encodes python dict as http response
        (for now, only json is supported)
        """
        response = response or {'status': 200}
        if 'status' not in response: response['status'] = 200
        return HTTPResponse(
            json.dumps(response),
            status=response['status'],
            content_type='application/json',
        )
