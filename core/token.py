from arrow.arrow import timedelta
from arrow import utcnow
import settings  # TODO: FIX ???
import jwt


class Token:
    """
    API token wrapper
    """

    ALGORITHM = 'HS256'
    EXPIRE = timedelta(hours=24)
    USER, SERVICE, ADMIN = 0x0, 0x1, 0xF
    TYPES = {
        'USER': USER,
        'SERVICE': SERVICE,
        'ADMIN': ADMIN,
    }

    def __init__(self, string):
        self.string = string
        self.valid = None
        self.expired = None
        self.type = None
        self.uid = None
        self.sid = None
        self.validate()

    def __repr__(self):
        reverse = [k for k, v in self.TYPES.items() if v == self.type]
        type = reverse[0] if reverse else self.type
        args = ', '.join((
            f'type={type}',
            f'uid={self.uid}',
            f'sid={self.sid}',
            f'valid={self.valid}',
            f'expired={self.expired}',
        ))
        return 'Token(%s)' % args

    def __str__(self): return self.string

    def validate(self):
        try:
            data = jwt.decode(
                jwt=self.string,
                key=settings.SECRET,
                algorithms=[self.ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            self.valid = False
            self.expired = True
            return
        except jwt.InvalidTokenError:
            self.valid = False
            return

        self.valid = True
        self.expired = False
        self.uid = data.get('uid')
        self.sid = data.get('sid')
        self.type = data.get('typ')

    @classmethod
    def create(cls, uid=None, sid=None, type=None, expire=None, **data):
        if uid is not None: data['uid'] = uid
        if sid is not None: data['sid'] = sid
        if type is None: type = cls.USER
        if expire is None: expire = cls.EXPIRE
        if isinstance(type, str): type = cls.TYPES[type.upper()]
        data['exp'] = (utcnow() + expire).naive
        data['typ'] = type
        token = jwt.encode(
            payload=data,
            key=settings.SECRET,
            algorithm=cls.ALGORITHM,
        ).decode()
        return cls(token)
