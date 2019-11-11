from .router import Router
from .environ import env

from concurrent import futures
from easydict import EasyDict
from aiohttp import web
import importlib
import asyncio


class Application:
    def __init__(self, settings=None, loop=None, router=None):
        self.settings = self._get_settings(settings)
        # TODO: LOGGER
        self.loop = loop or self._get_loop()
        self.app = web.Application()
        # TODO: DECOUPLE ROUTER
        self.router = router or Router(self.app)
        self.executor = futures.ProcessPoolExecutor()
        self.loop.set_default_executor(self.executor)
        # TODO: SIGNALS
        # TODO: ROUTE METHOD

    def _get_loop(self):
        """
        Constructs new async event loop,
        using uvloop speedup if possible
        """
        try:
            import uvloop
            loop = uvloop.new_event_loop()
        except ImportError:
            loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

    def _get_settings(self, settings):
        """
        Prepares settings dict (easydict)
        """
        if isinstance(settings, dict):
            return EasyDict(**settings)

        try:
            settings = settings or env.str('SETTINGS', 'settings')
            module = importlib.import_module(settings)
            attrs = {
                k: v for k, v in module.__dict__.items()
                if k[0] != '_' and k.isupper()
            }
        except ImportError:
            raise RuntimeError(
                'Cannot import settings module (%s) - '
                'check SETTINGS environment variable' % settings
            )

        # TODO: BASE SETTINGS
        settings = EasyDict()
        settings.update(**attrs)
        return settings

    def run(self):
        """
        Launch application event loop and start serving
        """
        # TODO: UPDATE ROUTER BEFORE START
        web.run_app(
            self.app,
            host=self.settings.HOST,
            port=self.settings.PORT,
        )

    async def execute(self, func, *args):
        """
        Run function in app's default executor
        """
        return await self.loop.run_in_executor(
            executor=self.executor, func=func, *args
        )
