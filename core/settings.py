from .environ import env
import importlib

module = env.str('SETTINGS', 'settings').rstrip('.py')
settings = importlib.import_module(module).__dict__


def __getattr__(name):
    if name not in settings:
        raise KeyError('Unknown setting: %s' % name)
    return settings[name]
