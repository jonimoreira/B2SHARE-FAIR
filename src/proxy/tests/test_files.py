from fair.models import CommunityModel
import datetime
import statistics
from pyld import jsonld

def test_get_file_by_id(client):
    result = client.simulate_get(
        '/files/c89a695c-f4c7-4ee5-a4b0-eda2f79dbdd9')

    assert result is not None


def test_performance_get_id_files(client):
    numCalls = 10
    numCallsBlocks = 10

    community_ids = ["88699ea0-e199-43f7-8a16-d311ecfa02e1", "5c11832e-444d-4740-8bdc-1fb55d12eeef", "25486e34-4f9c-4605-b0a5-f5f7e48d11b2", "c89a695c-f4c7-4ee5-a4b0-eda2f79dbdd9", "940fa97e-9a79-4ec0-9327-8f6b0b504b41", "eb6ebb0f-6b33-4972-87dd-78e6e281d3b9", "f91a4583-6f7e-4e6a-9bde-c75a635a4cef", "9bd0a681-d93f-46f9-8b37-c67e6edee571", "2d3af417-0de0-4b88-86d9-320b2084a945", "d5001514-5f6f-47f5-8ec2-5ed8c3629b7f"]
    results = []
    for file_id in file_ids:
        for i in range(1,numCallsBlocks):
            result = compute_difference(numCalls, file_id)
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

    assert False



def compute_difference(numCalls, _id):
    urlFdp = 'http://localhost:8000/distributions/' + _id
    urlB2 = 'https://trng-b2share.eudat.eu/api/files/' + _id

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
