"""
Custom mini-router
"""

from sanic.response import HTTPResponse
from core.views import View, APIError
import json


class Router:
    """
    Custom mini-router, supporting:
    + Registering package of views
    + Request decoding & encoding
    + URL prefix (may be useful for versioning)
    - Multiple decoding & encoding options
    - IP-based BadRPS limiting
    """

    METHODS = ['GET', 'POST']

    def __init__(self, app, prefix=''):
        self.app = app
        self.views = {}
        self.app.add_route(self.handle, prefix + '/', self.METHODS)
        self.app.add_route(self.handle, prefix + '/<path:path>', self.METHODS)

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
        data = self.decode(request)
        if data is None:
            # TODO: Logging
            response = APIError('Bad request', 400).response
            return self.encode(response)
        method = path.replace('/', '.').strip('.')
        method = method or data.pop('method', '')
        if not method or method not in self.views:
            # TODO: Logging
            response = APIError('Unknown method', 404).response
            return self.encode(response)
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
