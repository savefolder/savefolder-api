"""
Dynamically imported settings
"""

from easydict import EasyDict
from .environ import env
import importlib

module = env.str('SETTINGS', 'settings').rstrip('.py')
settings = importlib.import_module(module)
settings = EasyDict(settings.__dict__)
