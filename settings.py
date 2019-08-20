"""
Global settings live here
"""

from core.environ import env

SECRET = env.str('SECRET')
HOST = env.str('HOST', '0.0.0.0')
PORT = env.int('PORT', 80)
