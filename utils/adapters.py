"""
Communication protocol adapters
-------------------------------
An adapter handles duplex conversion between multiple protocols and message formats,
so that API logic is fully protocol-independent and operates only with clean python dicts
"""

from sanic.request import Request
from sanic.response import json
from sanic.app import Sanic


class HTTPAdapter:
    """
    Handles HTTP traffic
    """

    def __init__(self, app: Sanic, router):
        self.app = app
        self.router = router

    def install(self):
        # TODO: Move '/api' to settings
        self.app.router.add('/api', ['POST'], self.handle)

    async def handle(self, request: Request):
        content = request.headers.get('content-type', 'application/json')

        if content == 'application/json': response = await self.handle_json(request)
        elif content == 'multipart/form-data': response = await self.handle_multipart(request)
        else: response = {'error': 'Content type not supported', 'status': 406}

        status = response.pop('status', 200)
        response = json(response, status=status)  # TODO: [!] This is synchronous
        return response

    async def handle_json(self, request: Request):
        data = request.json  # TODO: [!] This is synchronous, possible OOM
        response = await self.router.handle(data)
        return response

    async def handle_multipart(self, request: Request):
        form = request.form  # TODO: [!] This is synchronous, possible OOM
        pass  # TODO


class WSAdapter:
    """
    Handles WebSocket traffic
    """

    def __init__(self, app: Sanic, router):
        self.app = app
        self.router = router

    def install(self):
        pass  # TODO

    async def handle_connect(self, request):
        pass  # TODO

    async def handle_message(self, message):
        pass  # TODO
