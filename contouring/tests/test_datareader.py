import pytest
from contouring import datareader
import os
from datetime import timezone
import xml.etree.ElementTree as ET

FIXTURE_DIR = os.path.dirname(os.path.realpath(__file__))

# Import the class whose method is mocked
from owslib.feature.common import WFSCapabilitiesReader

@pytest.fixture()
def mock_capabilities(monkeypatch):
    # Creating a new Datareader object creates a GetCapabilities request 
    # through owslib. Make a spoof for capabilities results 

    def mock_read(*args, **kwargs):
        # data_file = os.path.join(FIXTURE_DIR, 'mock_capabilities.xml')
        filepath = os.path.join(FIXTURE_DIR, 'mock_capabilities.xml')
        tree = ET.parse(filepath)
        return tree.getroot()

    monkeypatch.setattr(WFSCapabilitiesReader, "read", mock_read)

def test_datareader_class(mock_capabilities):
    # Dodge timeout errors from owslib for nonsense url with mock_capabilities
    dr = datareader.Datareader("https://fakeurl/wfs")
    assert dr.wfs.url == 'https://fakeurl/wfs'
    assert dr.wfs.version == '2.0.0'
    dr.stored_query_params.starttime = "2017-08-01T00:00:00Z"
    assert dr.stored_query_params.starttime == "2017-08-01T00:00:00Z"
    dr.stored_query_params.starttime = "2017-08-01T01:00:00Z"
    assert dr.stored_query_params.starttime == "2017-08-01T01:00:00Z"


def test_starttimes():
    starttimes = datareader.starttimes(2017, 8)
    mytime = next(starttimes)
    assert mytime.year == 2017
    assert mytime.month == 8
    assert mytime.hour == 0
    assert mytime.minute == 0
    assert mytime.tzinfo == timezone.utc
    mytime = next(starttimes)
    assert mytime.hour == 1


# class TestResource(object):
# @pytest.fixture
# def windgust_multi_contours():
#     with open(data_file, 'r') as f:
#         wfs_data = f.read()
#     f.closed
#     return wfs_data

# @pytest.fixture
# def windgust_multi_contours():
#     data_file = os.path.join(FIXTURE_DIR, 'windgustcoverage_contours_0-5_5-10_10-15.xml')
#     with open(data_file, 'r') as f:
#         wfs_data = f.read()
#     f.closed
#     return wfs_data

# # custom class to be the mock return value of WebFeatureService.getfeature()
# class MockResponse():
#     """Define methods that are required in tests"""
#     @staticmethod
#     def read():
#         return windgust_multi_contours


# # monkeypatched WebFeatureService.getfeature as fixture
# @pytest.fixture
# def mock_response(monkeypatch):
#     """WebFeatureService.getfeature() mocked to return some wfs-data."""

#     def mock_get(*args, **kwargs):
#         return MockResponse()

#     monkeypatch.setattr(WebFeatureService, "getfeature", mock_get)

# notice our test uses the custom fixture instead of monkeypatch directly
# def test_get_json(mock_response):
#     dr = Datareader()
#     result = dr.getWFS("juttu", {'juttu': 'homma'})
#     assert result["mock_key"] == "mock_response"

