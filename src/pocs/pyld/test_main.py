import unittest
from main import Model, Field, NestedField

from pyld import jsonld
import json

class NestedModel(Model):
    name = Field(name='name')
    description = Field(name='description')


class MockModel(Model):
    name = Field(name='name')
    resource_name = 'communities'


class LinksModel(Model):
    selflink = Field(name='self')

    def __repr__(self):
        return '{"self": "%s"}' % self.selflink

class MockModelWithNested(MockModel):
    nested = NestedField(name='roles', cls=NestedModel, multiple=True)
    links = NestedField(name='links', cls=LinksModel)

class WebAppModel(Model):
    """
    B2Share webapp model schema abstraction.
    """

    identifier = Field(name='id')
    name = Field(name='name')
    description = Field(name='description')
    created = Field(name='created')
    updated = Field(name='updated')

    site_function = Field(name='site_function')
    training_site_link = Field(name='training_site_link')
    version = Field(name='version')

    resource_name = ''

class CommunityModel(Model):
    """
    B2Share community model schema abstraction.
    """

    identifier = Field(name='id')
    name = Field(name='name')
    description = Field(name='description')
    created = Field(name='created')
    updated = Field(name='updated')
    logo = Field(name='logo')
    publication_workflow = Field(name='publication_workflow')
    restricted_submission = Field(name='restricted_submission')
    links = NestedField(name='links', cls=LinksModel)

    resource_name = 'communities'

class RecordModel(Model):
    """
    B2Share record model schema abstraction.
    """

    identifier = Field(name='id')
    name = Field(name='name')
    description = Field(name='description')
    created = Field(name='created')
    updated = Field(name='updated')

    links = NestedField(name='links', cls=LinksModel)

    resource_name = 'records'


class FileModel(Model):
    """
    B2Share file model schema abstraction.
    """

    identifier = Field(name='id')
    name = Field(name='name')
    description = Field(name='description')
    created = Field(name='created')
    updated = Field(name='updated')

    links = NestedField(name='links', cls=LinksModel)

    resource_name = 'files'

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.url = 'https://trng-b2share.eudat.eu/api/communities/'

    def tearDown(self):
        pass

    def test_load_mock_model(self):
        model = MockModel.from_dict({'name': 'Aalto'})
        self.assertEqual(model.name, 'Aalto')

    def test_load_community_model(self):
        models = list(CommunityModel.get_all())
        model = models[0]
        self.assertEqual(model.name, 'Aalto')
        print(model.__dict__)

    def test_load_communities(self):
        models = list(MockModel.get_all())
        self.assertEqual(len(models), 13)

    def test_multiple_nested_model(self):
        models = list(MockModelWithNested.get_all())
        nested = models[0].nested[0]
        print(nested.name);
        self.assertTrue(nested.name.endswith(':admin') or nested.name.endswith(':member'))

    def test_single_nested_model(self):
        models = list(MockModelWithNested.get_all())
        links = models[0].links
        self.assertTrue(isinstance(links.selflink, str))

    # Test L1 translation
    def test_translate_webapp(self):
        models = list(WebAppModel.get_all())
        print(len(models))

    # Test L2 translation
    def test_translate_communities(self):
        models = list(CommunityModel.get_all())
        #import pdb; pdb.set_trace()

        for community in models:
            #print(community.links.selflink)
            translate_catalog(community)
            #print(community.identifier)

    # Test L3 translation
    def test_translate_records(self):
        models = list(RecordModel.get_all())
        for record in models:
            print(record.name)
            translate_dataset(record)

        print(len(models))

    # Test L4 translation
    def test_translate_files(self):
        models = list(FileModel.get_all())
        print(len(models))

# B2SHARE: webapp
# Level 1: FAIR Data Point metadata layer (data repository)
def translate_fdp(webapp):
    context = {
        # ontologies used in FDP according to spec
        "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs" : "http://www.w3.org/2000/01/rdf-schema#",
        "dcat" : "http://www.w3.org/ns/dcat#",
        "xsd" : "http://www.w3.org/2001/XMLSchema#",
        "owl" : "http://www.w3.org/2002/07/owl#",
        "dct" : "http://purl.org/dc/terms/",
        "lang" : "http://id.loc.gov/vocabulary/iso639-1/",
        "fdp" : "http://rdf.biosemantics.org/ontologies/fdp-o#",
        "r3d" : "http://www.re3data.org/schema/3-0#",
        "foaf" : "http://xmlns.com/foaf/",
        # B2SHARE otology (internal terms)
        "b2" : "https://b2share.eudat.eu/ontology/b2share/" }
    doc = {
        "@type": "r3d:Repository",
        "http://purl.org/dc/terms/identifier": webapp.identifier,
        "http://purl.org/dc/terms/title": webapp.name,
        "http://purl.org/dc/terms/description": webapp.description,
        "http://purl.org/dc/terms/issued": webapp.created,
        "http://purl.org/dc/terms/modified": webapp.updated,

        "https://b2share.eudat.eu/ontology/b2share/site_function" : webapp.site_function
    }
    compacted = jsonld.compact(doc, context)
    print(compacted)
    return compacted


# B2SHARE: Community
# Level 2: Catalog metadata layer
def translate_catalog(community):
    context = {
        # ontologies used in FDP according to spec
        "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs" : "http://www.w3.org/2000/01/rdf-schema#",
        "dcat" : "http://www.w3.org/ns/dcat#",
        "xsd" : "http://www.w3.org/2001/XMLSchema#",
        "owl" : "http://www.w3.org/2002/07/owl#",
        "dct" : "http://purl.org/dc/terms/",
        "lang" : "http://id.loc.gov/vocabulary/iso639-1/",
        "fdp" : "http://rdf.biosemantics.org/ontologies/fdp-o#",
        "foaf" : "http://xmlns.com/foaf/",
        # B2SHARE otology (internal terms)
        "b2" : "https://b2share.eudat.eu/ontology/b2share/",
        # Other ontologies (reused)
        "pro" : "http://purl.org/spar/pro/" }

    doc = {
        "@type": "dcat:Catalog",
        "http://purl.org/dc/terms/identifier": community.identifier,
        "http://purl.org/dc/terms/title": community.name,
        "http://purl.org/dc/terms/description": community.description,
        "http://purl.org/dc/terms/issued": community.created,
        "http://purl.org/dc/terms/modified": community.updated,
        "http://xmlns.com/foaf/logo" : community.logo,
        "https://b2share.eudat.eu/ontology/b2share/publication_workflow" : community.publication_workflow,
        "https://b2share.eudat.eu/ontology/b2share/restricted_submission" : community.restricted_submission,
        "@id": community.links.selflink
    }
    compacted = jsonld.compact(doc, context)
    print(compacted)
    return compacted

# B2SHARE: Record
# Level 3: Dataset metadata layer
def translate_dataset(record):
    context = {
        # ontologies used in FDP according to spec
        "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs" : "http://www.w3.org/2000/01/rdf-schema#",
        "dcat" : "http://www.w3.org/ns/dcat#",
        "xsd" : "http://www.w3.org/2001/XMLSchema#",
        "owl" : "http://www.w3.org/2002/07/owl#",
        "dct" : "http://purl.org/dc/terms/",
        "lang" : "http://id.loc.gov/vocabulary/iso639-1/",
        "fdp" : "http://rdf.biosemantics.org/ontologies/fdp-o#",
        "foaf" : "http://xmlns.com/foaf/",
        # B2SHARE otology (internal terms)
        "b2" : "https://b2share.eudat.eu/ontology/b2share/"
        # Other ontologies (reused)
        }

    doc = {
        "@type": "dcat:Dataset",
        "http://purl.org/dc/terms/identifier": record.identifier,
        "http://purl.org/dc/terms/title": record.name,
        "http://purl.org/dc/terms/description": record.description,
        "http://purl.org/dc/terms/issued": record.created,
        "http://purl.org/dc/terms/modified": record.updated,
        "@id": record.links.selflink
    }
    compacted = jsonld.compact(doc, context)
    print(compacted)
    return compacted


if __name__ == "__main__":
    unittest.main()
