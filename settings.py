"""
Global settings live here
"""

from core.utils import env

# TODO: Get rid of envparse (abandoned trash)
SECRET = env.str('SECRET')
HOST = env.str('HOST', default='0.0.0.0')
PORT = env.int('PORT', default=80)
