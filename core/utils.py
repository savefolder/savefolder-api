"""
Miscellaneous utils
"""

from envparse import Env
import warnings
import os


class Environ(Env):
    """
    Thin envparse wrapper
    """

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


env = Environ()
env.read_envfile()
