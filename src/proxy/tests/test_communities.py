from fair.models import CommunityModel
import datetime
import statistics
from pyld import jsonld

def test_get_all_communities(client):
    result = client.simulate_get('/catalogs')

    assert len(result.json) == 14


def test_get_community_by_id(client):
    result = client.simulate_get(
        '/catalogs/c4234f93-da96-4d2f-a2c8-fa83d0775212')

    assert result.json['dct:title'] == 'Aalto'


def test_performance_get_all_catalogs(client):
    numCalls = 3
    numCallsBlocks = 3

    results = []
    for i in range(1,numCallsBlocks):
        result = compute_difference(numCalls, "")
        results.append(result)
        print("Time difference of FDP compared to B2 (%): " + str(result))

    # Remove anomalies
    std_dev = statistics.stdev(results)
    mean = statistics.mean(results)
    anomalies = 0
    filteredResults = []
    for result in results:
        if result > mean + std_dev:
            anomalies += 1
        elif result < mean - std_dev:
            anomalies += 1
        else:
            filteredResults.append(result)

    avg_percent = statistics.mean(filteredResults)
    print("Average (%): " + str(avg_percent))
    print("Anomalies: " + str(anomalies))

    #assert False


def test_performance_get_id_catalogs(client):
    numCalls = 10
    numCallsBlocks = 10
    compute_performance_get_id_catalogs(numCalls, numCallsBlocks)

    numCalls = 10
    numCallsBlocks = 50
    compute_performance_get_id_catalogs(numCalls, numCallsBlocks)

    numCalls = 10
    numCallsBlocks = 100
    compute_performance_get_id_catalogs(numCalls, numCallsBlocks)

    assert False


def compute_performance_get_id_catalogs(numCalls, numCallsBlocks):
    community_ids = ["c4234f93-da96-4d2f-a2c8-fa83d0775212", "99916f6f-9a2c-4feb-a342-6552ac7f1529", "0afede87-2bf2-4d89-867e-d2ee57251c62", "94a9567e-2fba-4677-8fde-a8b68bdb63e8", "b344f92a-cd0e-4e4c-aa09-28b5f95f7e41"]

    for community_id in community_ids:
        results = []
        for i in range(1,numCallsBlocks):
            result = compute_difference(numCalls, community_id)
            results.append(result)
            #print("Time difference of FDP compared to B2 (%): " + str(result))

        # Remove anomalies
        std_dev = statistics.stdev(results)
        mean = statistics.mean(results)
        anomalies = 0
        filteredResults = []
        for result in results:
            if result > mean + std_dev:
                anomalies += 1
            elif result < mean - std_dev:
                anomalies += 1
            else:
                filteredResults.append(result)

        avg_percent = statistics.mean(filteredResults)
        print("Average (%): " + str(avg_percent))
        print("Anomalies: " + str(anomalies))
    #return avg_percent
    #assert False


"""
print("================== RESULTS =========================")
print("Number calls: " + str(numCalls))
print("Total time FDP (ms): " + str(total_ms_A_01))
print("Average time FDP (ms): " + str(avg_ms_A_01))
print("Total time B2 (ms): " + str(total_ms_B_01))
print("Average time B2 (ms): " + str(avg_ms_B_01)) """

def compute_difference(numCalls, _id):
    urlFdp = 'http://localhost:8000/catalogs/' + _id
    urlB2 = 'https://trng-b2share.eudat.eu/api/communities/' + _id

    total_ms_A_01 = compute_calls(urlFdp, numCalls)
    avg_ms_A_01 = total_ms_A_01/numCalls

    total_ms_B_01 = compute_calls(urlB2, numCalls)
    avg_ms_B_01 = total_ms_B_01/numCalls

    result = total_ms_A_01*100/total_ms_B_01

    return result


def compute_calls(uri, numCalls):

    start = datetime.datetime.now()
    for i in range(1,numCalls):
        doc = jsonld.get_document_loader()(uri)
        #doc = CommunityModel.load_document(uri)
        #adding some minimal processing
        if doc['document'] is None:
            print("Error loading the URL: " + uri)

    end = datetime.datetime.now()
    diff = end - start
    total_ms = diff.total_seconds() * 1000

    return total_ms
