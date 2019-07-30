"""
API method implementations live here
"""


class UploadView:
    method = 'images.upload'
    limiting = ['10 / min', '1000 / day']  # TODO: Think aboud'it
    schema = {  # TODO: Add more constraints, move schema to settings?
        'file': {'type': 'string', 'required': True},  # TODO: What about multipart? Custom cerberus type maybe?
        'rid': {'type': 'string'},  # TODO: What about rid uniqueness?
        'tags': {
            'type': 'list',
            'schema': {'type': 'string'},
        },
    }


class UpdateView:
    method = 'images.update'
    limiting = ['100 / sec']  # TODO: Default 'just-dont-ddos' will do?
    schema = {
        'id': {'type': 'string'},
        'rid': {'type': 'string'},
        'tags': {
            'type': 'list',
            'schema': {'type': 'string'},
        },
        'delete': {'type': 'boolean'},
    }


class SearchView:
    method = 'images.search'
    limiting = 'just-dont-ddos'
    schema = {
        'query': {'type': 'string'},
        'id': {'type': 'string'},
        'rid': {'type': 'string'},
    }


class TokenView:
    admin = True
    schema = {
        'rid': {'type': 'string', 'required': True}
    }
