from fair.models import CommunityModel
import datetime
import statistics

def test_get_fdp(client):
    result = client.simulate_get('/fdp')

    assert result.json is not None


def test_performance_get_fdp(client):
    numCalls = 3
    numCallsBlocks = 3

    results = []
    for i in range(1,numCallsBlocks):
        result = compute_difference(numCalls)
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


def compute_difference(numCalls):
    urlFdp = 'http://localhost:8000/fdp/'
    urlB2 = 'https://trng-b2share.eudat.eu/api/'

    total_ms_A_01 = compute_calls(urlFdp, numCalls)
    avg_ms_A_01 = total_ms_A_01/numCalls

    total_ms_B_01 = compute_calls(urlB2, numCalls)
    avg_ms_B_01 = total_ms_B_01/numCalls

    result = total_ms_A_01*100/total_ms_B_01

    return result


def compute_calls(url, numCalls):

    start = datetime.datetime.now()
    for i in range(1,numCalls):
        doc = CommunityModel.load_document(url)
        #adding some minimal processing
        if doc['document'] is None:
            print("Error loading the URL: " + url)

    end = datetime.datetime.now()
    diff = end - start
    total_ms = diff.total_seconds() * 1000

    return total_ms
