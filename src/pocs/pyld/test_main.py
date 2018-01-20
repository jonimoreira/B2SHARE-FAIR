import unittest
from main import Model, Field, NestedField

from pyld import jsonld
import json

CONST_NUM_COMMUNITIES = 14

# base URL for tests: https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095

#For interacting with B2SHARE via external services or applications. GET methods:
# Level 1: webapp --> FDP (data repository)
#  o Get web applicaton: /api/
    # test_translate_webapp

#[ok] o List all communities: /api/communities
    # test_translate_communities
#[ok] o Get a community: /api/communities/@CommunityID
    # test_translate_community
#o Get community schema: /api/communities/$COMMUNITY_ID/schemas/last
#o List all records: /api/records
#o List records per community: /api/records/?q=community:COMMUNITY_ID
#o Search records: /api/records/?q=$QUERY_STRING
#o Search drafts: /api/records/?drafts
#o Get a specific record: /api/record/RECORD_ID
#o List the files uploaded into a record object: /api/files/FILE_BUCKET_ID

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
    CONST_B2SHARE_REPOSITORY_ID = "EUDAT_B2SHARE_WEBAPP"
    CONST_B2SHARE_REPOSITORY_NAME = "EUDAT B2SHARE data repository"
    CONST_B2SHARE_REPOSITORY_DESCRIPTION = "The EUDAT B2SHARE data repository as a web application"
    CONST_B2SHARE_REPOSITORY_CREATED = "01/01/2018"
    CONST_B2SHARE_REPOSITORY_UPDATED = "01/01/2018"

    identifier = CONST_B2SHARE_REPOSITORY_ID # Field(name='id')
    name = CONST_B2SHARE_REPOSITORY_NAME #Field(name='name')
    description = CONST_B2SHARE_REPOSITORY_DESCRIPTION # Field(name='description')
    created = CONST_B2SHARE_REPOSITORY_CREATED # Field(name='created')
    updated = CONST_B2SHARE_REPOSITORY_UPDATED # Field(name='updated')
    publisher = ''

    site_function = Field(name='site_function')
    training_site_link = Field(name='training_site_link')
    version = Field(name='version')
    b2access_registration_link = Field(name='b2access_registration_link')
    b2note_url = Field(name='b2note_url')
    terms_of_use_link = Field(name='terms_of_use_link')

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
        #print(model.__dict__)

    def test_load_communities(self):
        models = list(MockModel.get_all())
        self.assertEqual(len(models), CONST_NUM_COMMUNITIES)

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
        webapp = WebAppModel.get('')
        fdp_repository = translate_fdp(webapp)
        print(fdp_repository)

    # Test L2 translation: List all communities: /api/communities
    def test_translate_communities(self):
        models = list(CommunityModel.get_all())
        #import pdb; pdb.set_trace()

        for community in models:
            #print(community.links.selflink)
            catalog = translate_catalog(community)
            assert_fields_community_catalog(self, community, catalog)
            #print(community.identifier)

    # Test L2 translation: List all communities: /api/communities
    def test_translate_community(self):
        community = CommunityModel.get_id('e9b9792e-79fb-4b07-b6b4-b9c2bd06d095')
        #print(community)
        catalog = translate_catalog(community)
        #print(catalog['dct:title'])
        assert_fields_community_catalog(self, community, catalog)

    # Test L3 translation
    def test_translate_records(self):
        models = list(RecordModel.get_all())
        for record in models:
            print(record.name)
            translate_dataset(record)

        #print(len(models))

    # Test L4 translation
    def test_translate_files(self):
        models = list(FileModel.get_all())
        #print(len(models))

    # Test open JSON file
    def test_open_json_file(self):
        with open('b2_community_EUDAT_e9b9792e-79fb-4b07-b6b4-b9c2bd06d095.json') as json_data:
            d = json.load(json_data)
            #print(d)
            self.assertEqual(True, True)

    # Test community translation from JSON file (local)
    def test_translate_community_json_file(self):
        community = CommunityModel.get_from_file('b2_community_EUDAT_e9b9792e-79fb-4b07-b6b4-b9c2bd06d095.json')
        catalog = translate_catalog(community)
        print(catalog['@type'])
        print(catalog['dct:title'])
        assert_fields_community_catalog(self, community, catalog)
        #self.assertEqual(catalog['name'], community.name)


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
        "http://purl.org/dc/terms/description": webapp.description,
        "http://purl.org/dc/terms/title": webapp.name,
        "http://purl.org/dc/terms/hasVersion": webapp.version,
        "http://purl.org/dc/terms/publisher": webapp.publisher,

        "http://purl.org/dc/terms/issued": webapp.created,
        "http://purl.org/dc/terms/modified": webapp.updated,

        "https://b2share.eudat.eu/ontology/b2share/site_function" : webapp.site_function,
        "https://b2share.eudat.eu/ontology/b2share/training_site_link" : webapp.training_site_link,
        "https://b2share.eudat.eu/ontology/b2share/b2access_registration_link" : webapp.b2access_registration_link,
        "https://b2share.eudat.eu/ontology/b2share/b2note_url" : webapp.b2note_url,
        "https://b2share.eudat.eu/ontology/b2share/terms_of_use_link" : webapp.terms_of_use_link

    }
'''
TODO:
    r3d:dataCatalog <http://dev-vm.fair-dtls.surf-hosted.nl:8082/fdp/biobank> , <http://dev-vm.fair-dtls.surf-hosted.nl:8082/fdp/comparativeGenomics> , <http://dev-vm.fair-dtls.surf-hosted.nl:8082/fdp/patient-registry> , <http://dev-vm.fair-dtls.surf-hosted.nl:8082/fdp/textmining> , <http://dev-vm.fair-dtls.surf-hosted.nl:8082/fdp/transcriptomics> ;
	r3d:institution <http://dtls.nl> ;
	r3d:institutionCountry <http://lexvo.org/id/iso3166/NL> ;
	r3d:lastUpdate "2016-10-27"^^xsd:date ;
	r3d:startDate "2016-10-27"^^xsd:date ;
	rdfs:label "DTL FAIR Data Point"@en .
'''

    compacted = jsonld.compact(doc, context)
    #print(compacted)
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
    #print(compacted)
    return compacted

# Test mappings Level 2: Catalog x Community, according to translate_catalog method
def assert_fields_community_catalog(self, community, catalog):
    self.assertEqual(community.identifier, catalog["dct:identifier"])
    self.assertEqual(community.name, catalog["dct:title"])
    self.assertEqual(community.description, catalog["dct:description"])
    self.assertEqual(community.created, catalog["dct:issued"])
    self.assertEqual(community.updated, catalog["dct:modified"])
    self.assertEqual(community.logo, catalog["foaf:logo"])
    self.assertEqual(community.publication_workflow, catalog["b2:publication_workflow"])
    #self.assertEqual(community.restricted_submission, catalog["b2:restricted_submission"])

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
    #print(compacted)
    return compacted


if __name__ == "__main__":
    unittest.main()
