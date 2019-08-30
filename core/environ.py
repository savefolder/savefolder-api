import urllib.parse as urlparse
from envparse import Env
import json as pyjson
import warnings
import os


def shortcut(cast):
    # Fix: `default` kwarg is always second argument
    # So you can do `env.whatever('KEY', 'DEFAULT')`
    def method(self, var, default=None, **kwargs):
        return self.__call__(var, cast=cast, default=default, **kwargs)
    return method


class Environ(Env):
    """
    Thin envparse wrapper
    """

    # Improved shortcuts
    bool = shortcut(bool)
    dict = shortcut(dict)
    float = shortcut(float)
    int = shortcut(int)
    list = shortcut(list)
    str = shortcut(str)
    json = shortcut(pyjson.loads)
    url = shortcut(urlparse.urlparse)

    def read_envfile(self, path=None, **overrides):
        # Temporarily proxy `setdefault` to `setitem`
        # So that .env file priority is higher
        setdefault = os.environ.setdefault
        os.environ.setdefault = os.environ.__setitem__
        with warnings.catch_warnings():
            # Get rid of annoying warning
            warnings.simplefilter('ignore')
            super().read_envfile(path=path, **overrides)
        os.environ.setdefault = setdefault


# Convenient global var
env = Environ()
env.read_envfile()
