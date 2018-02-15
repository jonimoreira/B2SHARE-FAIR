def test_get_all_communities(client):
    result = client.simulate_get('/community')

    assert len(result.json) == 14


def test_get_community_by_id(client):
    result = client.simulate_get(
        '/community/c4234f93-da96-4d2f-a2c8-fa83d0775212')

    assert result.json['dct:title'] == 'Aalto'

