"""
Custom mini-router
"""

from sanic.response import HTTPResponse
from .views import View, APIError
from .limiter import Limiter
import json


class Router:
    """
    Custom mini-router, supporting:
    + Registering package of views
    + Request decoding & encoding
    + URL prefix (may be useful for versioning)
    + IP-based BadRPS limiting
    - Multiple decoding & encoding options
    """

    METHODS = ['GET', 'POST']
    BAD_REQUESTS_LIMIT = ['500 / hour']

    def __init__(self, app, prefix=''):
        self.app = app
        self.views = {}
        self.limiter = Limiter(*self.BAD_REQUESTS_LIMIT, prefix='bad-requests')
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
        # Check if request ip behaved badly recently
        ip = request.remote_addr
        if ip and not await self.limiter.hit(ip, update=False):
            response = APIError('You got bamboozled', 503).response
            return self.encode(response)
        # Extract payload
        data = self.decode(request)
        if data is None:
            await self.limiter.hit(ip)
            response = APIError('Bad request', 400).response
            return self.encode(response)
        # Extract and validate target method
        method = path.replace('/', '.').strip('.')
        method = method or data.pop('method', '')
        if not method or method not in self.views:
            await self.limiter.hit(ip)
            response = APIError('Unknown method', 404).response
            return self.encode(response)
        # Handle & encode
        view = self.views[method]
        response = await view.handle(data)
        if response.get('status') == 403:
            # Not sure about that
            await self.limiter.hit(ip)
        return self.encode(response)

    def decode(self, request):
        """
        Decodes http request as python dict
        Supported encodings: json & query params
        """
        content = request.content_type
        try:
            if content == 'application/json': return request.json
            elif request.args: return request.args
            else: return {}
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
