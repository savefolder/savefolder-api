"""
Global settings live here
"""

from core.environ import env

SECRET = env.str('SECRET', 'super-secret-key')
HOST = env.str('HOST', '0.0.0.0')
PORT = env.int('PORT', 80)

TOKEN_EXPIRE = env.int('TOKEN_EXPIRE', 60 * 60 * 24)

REDIS_URL = env.str('REDIS_URL', 'redis://redis:6379')
MONGO_URL = env.str('MONGO_URL', 'mongodb://mongo:27017')

AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
AWS_BUCKET_NAME = env.str('AWS_BUCKET_NAME')
AWS_REGION_NAME = env.str('AWS_REGION_NAME')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
