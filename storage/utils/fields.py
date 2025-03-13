from django.db import models
from utils.string_utils import uuid_8


class IdField(models.CharField):
    """
    id = IdField()
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 8)
        kwargs['primary_key'] = kwargs.get('primary_key', True)
        kwargs['unique'] = kwargs.get('unique', True)
        kwargs['db_index'] = kwargs.get('db_index', True)
        kwargs['default'] = kwargs.get('default', uuid_8)
        kwargs['null'] = kwargs.get('null', False)
        kwargs['blank'] = kwargs.get('blank', False)
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'ID')
        kwargs['help_text'] = kwargs.get('help_text', 'ID')
        super().__init__(*args, **kwargs)