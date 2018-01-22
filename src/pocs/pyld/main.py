from pyld import jsonld
import json
from datetime import datetime

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

        return [self.cls.from_dict(item) for item in value.values()]


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

        for name, field in cls.get_fields():
            value = _dict.get(field.name)

            if value is not None:
                setattr(instance, name, field.parse(value))

        return instance


    @classmethod
    def get_all(cls):
        """gets all model intances from remote endpoint.

        :returns: list of cls instances.
        """
        url = '{url}{resource}'.format(url=CONST_BASE_URL, resource=cls.resource_name)
        doc = jsonld.get_document_loader()(url)

        for hit in doc['document']['hits']['hits']:
            # TODO: check if it is a valid path for all resources.
            yield cls.from_dict(hit)

    @classmethod
    def get_from_file(cls, _filename):
        with open(_filename) as json_data:
            d = json.load(json_data)
            return cls.from_dict(d)

    @classmethod
    def get_id(cls, object_id):
        url = '{url}{resource}/{id}'.format(url=CONST_BASE_URL, resource=cls.resource_name,id=object_id)
        doc = jsonld.get_document_loader()(url)
        return cls.from_dict(doc['document'])

    @classmethod
    def get(cls, _urlComplement):
        url = CONST_BASE_URL + _urlComplement
        doc = jsonld.get_document_loader()(url)
        return cls.from_dict(doc['document'])
