import os
import json

from pyld import jsonld

from fair.models import CommunityModel, RecordModel, WebAppModel
from fair.translators import assert_fields_community_catalog, translate_catalog, translate_fdp, translate_dataset, assert_fields_webapp_fdp


def get_data_file_path(data_file):
    cwd = os.path.dirname(__file__)
    paths = ['src', 'fair', 'tests']

    for p in paths:
        if p not in cwd:
            cwd = os.path.join(cwd, p)

    return os.path.join(cwd, 'data', data_file)


def test_load_community_model():
    models = list(CommunityModel.get_all())
    model = models[0]

    assert model.name == 'Aalto'

# Test L1 translation
def test_translate_webapp():
    webapp = WebAppModel.get('')
    fdp_repository = translate_fdp(webapp)
    assert_fields_webapp_fdp(webapp, fdp_repository)

# Test L2 translation: List all communities: /api/communities
def test_translate_communities():
    models = list(CommunityModel.get_all())

    for community in models:
        catalog = translate_catalog(community)
        assert_fields_community_catalog(community, catalog)

# Test L2 translation: List all communities: /api/communities
def test_translate_community():
    community = CommunityModel.get_id('e9b9792e-79fb-4b07-b6b4-b9c2bd06d095')
    catalog = translate_catalog(community)
    assert_fields_community_catalog(community, catalog)

# Test L3 translation
def test_translate_records():
    models = list(RecordModel.get_all())

    for record in models:
        translate_dataset(record)

# Test community translation from JSON file (local)
def test_translate_community_json_file():
    data_file = get_data_file_path('b2_community_EUDAT_e9b9792e-79fb-4b07-b6b4-b9c2bd06d095.json')

    community = CommunityModel.get_from_file(data_file)
    catalog = translate_catalog(community)

    assert_fields_community_catalog(community, catalog)
