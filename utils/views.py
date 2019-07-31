"""
Custom CBV implementation
"""


class BaseView:
    method = 'abstract'
    limiting = ['100 / sec']
    service = False
    schema = {}

    def __init_subclass__(cls):
        # TODO: ???
        pass
