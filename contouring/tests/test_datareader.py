import pytest
from contouring.datareader import Datareader
# contents of test_app.py, a simple test for our API retrieval
import pytest
import os
from datetime import timezone
FIXTURE_DIR = os.path.dirname(os.path.realpath(__file__))


# Import the class whose method is mocked
from owslib.wfs import WebFeatureService

def test_datareader_parameters():
    dr = Datareader('localhost')
    assert dr.service_url == 'localhost'
    assert dr.version == '2.0.0'

@pytest.fixture
def windgust_multi_contours():
    data_file = os.path.join(FIXTURE_DIR, 'windgustcoverage_contours_0-5_5-10_10-15.xml')
    with open(data_file, 'r') as f:
        wfs_data = f.read()
    f.closed
    return wfs_data

# custom class to be the mock return value of WebFeatureService.getfeature()
class MockResponse():
    """Define methods that are required in tests"""
    @staticmethod
    def read():
        return windgust_multi_contours


# monkeypatched WebFeatureService.getfeature as fixture
@pytest.fixture
def mock_response(monkeypatch):
    """WebFeatureService.getfeature() mocked to return some wfs-data."""

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(WebFeatureService, "getfeature", mock_get)


# notice our test uses the custom fixture instead of monkeypatch directly
# def test_get_json(mock_response):
#     dr = Datareader()
#     result = dr.getWFS("juttu", {'juttu': 'homma'})
#     assert result["mock_key"] == "mock_response"


def test_starttimes():
    dr = Datareader()
    starttimes = dr.starttimes(2017, 8)
    mytime = next(starttimes)
    assert mytime.year == 2017
    assert mytime.month == 8
    assert mytime.hour == 0
    assert mytime.minute == 0
    assert mytime.tzinfo == timezone.utc
    mytime = next(starttimes)
    assert mytime.hour == 1