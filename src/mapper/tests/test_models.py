import unittest
import json

from pyld import jsonld

from mapper import Model, Field, NestedField


CONST_NUM_COMMUNITIES = 14

# base URL for tests: https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095

"""
    For interacting with B2SHARE via external services or applications. GET methods:
    Level 1: webapp --> FDP (data repository)
        o Get web applicaton: /api/
            test_translate_webapp

    List all communities: /api/communities
        test_translate_communities

    Get a community: /api/communities/@CommunityID
        test_translate_community

    Get community schema: /api/communities/$COMMUNITY_ID/schemas/last
    List all records: /api/records
    List records per community: /api/records/?q=community:COMMUNITY_ID
    Search records: /api/records/?q=$QUERY_STRING
    Search drafts: /api/records/?drafts
    Get a specific record: /api/record/RECORD_ID
    List the files uploaded into a record object: /api/files/FILE_BUCKET_ID
"""


class MockModel(Model):
    name = Field(name='name')
    resource_name = 'communities'


class NestedModel(Model):
    name = Field(name='name')
    description = Field(name='description')


class MockModelWithNested(MockModel):
    nested = NestedField(name='roles', cls=NestedModel, multiple=True)


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.url = 'https://trng-b2share.eudat.eu/api/communities/'

    def tearDown(self):
        pass

    def test_load_mock_model(self):
        model = MockModel.from_dict({'name': 'Aalto'})
        self.assertEqual(model.name, 'Aalto')

    def test_load_communities(self):
        models = list(MockModel.get_all())
        self.assertEqual(len(models), CONST_NUM_COMMUNITIES)

    def test_multiple_nested_model(self):
        models = list(MockModelWithNested.get_all())
        nested = models[0].nested[0]
        self.assertTrue(
            nested.name.endswith(':admin') or nested.name.endswith(':member'))

    def test_single_nested_model(self):
        models = list(MockModelWithNested.get_all())

