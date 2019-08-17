"""
Custom logic level mini-router
"""


class Router:
    def __init__(self, app):
        self.app = app
        self.views = {}

    def register(self, view):
        handler = view.make_handler()
        self.views[view.method] = handler

    def handle(self, data):
        method = data.get('method')
        if method in self.views:
            handle = self.views[method]
            return await handle(data)
        return {'status': 404, 'error': 'Unknown method'}
