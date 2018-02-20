import json
from datetime import datetime

from pyld import jsonld
import falcon


CONST_BASE_URL = 'https://trng-b2share.eudat.eu/api/'


class Field:
    """basic model field representation

    """
    def __init__(self, name):
        self.name = name

    def parse(self, value):
        """usefull if we decide to set field types in the future.

        :value: str
        :returns: parsed value.

        """
        return value


class NestedField(Field):
    """basic nested field representation

    """
    def __init__(self, name, cls=None, multiple=False):
        super().__init__(name)
        self.cls = cls
        self.multiple = multiple

    def parse(self, value):
        if not self.multiple:
            return self.cls.from_dict(value)

        # check if we are dealing with an array or a dicticonary
        # based collection.
        flatarray = not hasattr(value, 'values')
        items = value if flatarray else value.values()
        return [self.cls.from_dict(item) for item in items]


class Model:
    @classmethod
    def get_fields(cls):
        """gets all fields from cls.

        :returns: dict.
        """
        yield from [
            (k,v) for k,v in cls.__dict__.items() if isinstance(v, Field)
        ]

    @classmethod
    def from_dict(cls, _dict):
        """creates a new instance based on a dicticonary.

        :returns: new cls instance.
        """

        instance = cls()

        if not _dict:
            _dict = {}

        for name, field in cls.get_fields():
            value = _dict.get(field.name)
            setattr(instance, name, field.parse(value))

        return instance

    @classmethod
    def get_from_file(cls, _filename):
        with open(_filename) as json_data:
            d = json.load(json_data)
            return cls.from_dict(d)

    @staticmethod
    def load_document(uri):
        doc = jsonld.get_document_loader()(uri)

        if doc['document'].get('status', 200) != 200:
            raise falcon.HTTPBadRequest(
                'Proxy Error',
                'An error has ocurred while requesting this resource.'
            )

        return doc

    @classmethod
    def get_all(cls, query=''):
        """gets all model intances from remote endpoint.

        :returns: list of cls instances.
        """
        uri = '{url}{resource}?{query}'.format(url=CONST_BASE_URL,
                                               resource=cls.resource_name, query=query,)
        doc = cls.load_document(uri)

        for hit in doc['document']['hits']['hits']:
            yield cls.from_dict(hit)

    @classmethod
    def get_id(cls, object_id):
        uri = '{url}{resource}/{id}'.format(url=CONST_BASE_URL, resource=cls.resource_name, id=object_id)
        doc = cls.load_document(uri)
        return cls.from_dict(doc['document'])

    @classmethod
    def get(cls, _urlComplement):
        url = CONST_BASE_URL + _urlComplement
        doc = jsonld.get_document_loader()(url)
        return cls.from_dict(doc['document'])
