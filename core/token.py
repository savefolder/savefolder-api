from datetime import datetime, timedelta
from .settings import settings
import jwt


class Token:
    """
    API token wrapper
    """

    ALGORITHM = 'HS256'
    DEFAULT_EXPIRE = timedelta(
        seconds=settings.TOKEN_EXPIRE
    )
    USER, SERVICE, ADMIN = range(3)
    ACCESS = {
        'USER': USER,
        'SERVICE': SERVICE,
        'ADMIN': ADMIN,
    }

    def __init__(self, string):
        self.string = string
        self.valid = None
        self.expired = None
        self.access = None
        self.uid = None
        self.sid = None
        self.validate()

    def __repr__(self):
        gen = (k for k, v in self.ACCESS.items() if v == self.access)
        access = next(gen, self.access)
        args = ', '.join((
            f'access={access}',
            f'uid={self.uid}',
            f'sid={self.sid}',
            f'valid={self.valid}',
            f'expired={self.expired}',
        ))
        return 'Token(%s)' % args

    def is_user(self):
        return self.access == self.USER

    def is_service(self):
        return self.access == self.SERVICE

    def is_admin(self):
        return self.access == self.ADMIN

    def __str__(self):
        return self.string

    def validate(self):
        try:
            data = jwt.decode(
                jwt=self.string,
                key=settings.SECRET,
                algorithms=[self.ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            self.valid = True
            self.expired = True
            return
        except jwt.InvalidTokenError:
            self.valid = False
            return

        self.valid = True
        self.expired = False
        self.uid = data.get('uid')
        self.sid = data.get('sid')
        self.access = data.get('acc')

    def check(self, access):
        if not self.valid: return False
        if type(access) == str: access = self.ACCESS[access.upper()]
        return self.access == access

    @classmethod
    def create(cls, uid=None, sid=None, access=None, expire=None, **data):
        if expire is None: expire = cls.DEFAULT_EXPIRE
        if access is None: access = cls.USER if uid else cls.SERVICE
        if type(access) == str: access = cls.ACCESS[access.upper()]

        if access == cls.USER and uid is None: raise KeyError('uid is required for user token')
        if access == cls.USER and sid is None: raise KeyError('sid is required for user token')
        if access == cls.SERVICE and sid is None: raise KeyError('sid is required for service token')

        if uid is not None: data['uid'] = str(uid)
        if sid is not None: data['sid'] = str(sid)
        data['exp'] = datetime.utcnow() + expire
        data['acc'] = access
        token = jwt.encode(
            payload=data,
            key=settings.SECRET,
            algorithm=cls.ALGORITHM,
        ).decode()
        return cls(token)
