from fair.models import CommunityModel
import datetime
import statistics
from pyld import jsonld

def test_get_all_records(client):
    result = client.simulate_get('/records')

    assert result is not None


def test_get_record_by_id(client):
    result = client.simulate_get(
        '/records/7547be3d2e93445783c4d343e6cdd1c0')

    assert result is not None


def test_performance_get_all_records(client):
    numCalls = 10
    numCallsBlocks = 10
    compute_performance_get_all_records(numCalls, numCallsBlocks)

    compute_performance_get_all_records(10, 50)
    compute_performance_get_all_records(10, 100)

    assert False


def test_performance_get_id_records(client):
    numCalls = 10
    numCallsBlocks = 10
    compute_performance_get_id_records(numCalls, numCallsBlocks)
    compute_performance_get_id_records(10, 50)
    compute_performance_get_id_records(10, 100)

    assert False


def test_performance_get_qs_records(client):
    numCalls = 10
    numCallsBlocks = 10
    compute_performance_get_qs_records(numCalls, numCallsBlocks)
    compute_performance_get_qs_records(10, 50)
    compute_performance_get_qs_records(10, 100)

    assert False


def compute_performance_get_all_records(numCalls, numCallsBlocks):
    record_ids = [""]
    compute_test_case(numCalls, numCallsBlocks,record_ids)


def compute_performance_get_id_records(numCalls, numCallsBlocks):
    record_ids = ["7547be3d2e93445783c4d343e6cdd1c0", "a11736ab1b174028a1bbedea63e84411", "ea735c4786f24ad4974fd7a58a7edc41", "3cb79e246ee34b3e9faaa3408feaf89e", "277e0971184242b1a80f4182e2f18aca", "b2246d077d3e4d9396a47393eb3ff952", "ad7cb0926f234428a850164e569e8162", "d3f5b834ce404c2db22e071f2a2b7c77", "7ab78a953116446a9a18d45f42ba86ef", "79e55266573546238e4c80e5233c2f68"]
    compute_test_case(numCalls, numCallsBlocks,record_ids)


def compute_performance_get_qs_records(numCalls, numCallsBlocks):
    record_ids = ["?page=2&size=10&sort=mostrecent&q=test", "?page=1&size=10&sort=mostrecent&q=community:99916f6f-9a2c-4feb-a342-6552ac7f1529"]
    compute_test_case(numCalls, numCallsBlocks,record_ids)


def compute_test_case(numCalls, numCallsBlocks,record_ids):
    results = []
    for record_id in record_ids:
        for i in range(1,numCallsBlocks):
            result = compute_difference(numCalls, record_id)
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
        print(record_id)
        print("Average (%): " + str(avg_percent))
        print("Anomalies: " + str(anomalies))


def compute_difference(numCalls, _qs):
    urlFdp = 'http://localhost:8000/datasets/' + _qs
    urlB2 = 'https://trng-b2share.eudat.eu/api/records/' + _qs

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
