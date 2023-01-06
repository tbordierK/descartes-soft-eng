from earthquakes.usgs_api import build_api_url


def test_no_param_query():
    endpoint = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
    params = {}
    expected_result = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    assert build_api_url(endpoint, params) == expected_result


def test_single_param_query():
    endpoint = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
    params = {"key1": "value1"}
    expected_result = "https://earthquake.usgs.gov/fdsnws/event/1/query?key1=value1"
    assert build_api_url(endpoint, params) == expected_result

    # Endpoint change
    endpoint = 'https://wildfires.usgs.gov/fdsnws/event/1/query'
    expected_result = "https://wildfires.usgs.gov/fdsnws/event/1/query?key1=value1"
    assert build_api_url(endpoint, params) == expected_result


def test_multi_param_query():
    endpoint = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
    params = {
        "longitude": 28,
        "latitude": 12,
    }
    expected_result = "https://earthquake.usgs.gov/fdsnws/event/1/query?longitude=28&latitude=12"
    assert build_api_url(endpoint, params) == expected_result


