ACCOUNT_TOKEN = {
    'id': {
        'type': 'string',
        'required': True,
    },
}

ACCOUNT_MERGE = {
    'key': {
        'type': 'integer',
    },
    'recreate_key': {
        'type': 'boolean',
    },
}

IMAGE_UPLOAD = {
    'url': {
        'type': 'string',
    },
    'base64': {
        'type': 'string',
    },
}

IMAGE_SEARCH = {
    'query': {
        'type': 'string',
        'maxlength': 256,
        'required': True,
    },
    'offset': {
        'type': 'integer',
    },
    'limit': {
        'type': 'integer',
        'min': 1,
        'max': 64,
    },
}
