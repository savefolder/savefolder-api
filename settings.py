"""
Global settings live here
"""

from core.environ import env

SECRET = env.str('SECRET')
HOST = env.str('HOST', '0.0.0.0')
PORT = env.int('PORT', 80)

REDIS_URL = env.str('REDIS_URL', 'redis://localhost')
MONGO_URL = env.str('MONGO_URL', 'mongodb://localhost')
