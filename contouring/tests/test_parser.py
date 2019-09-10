import pytest
import os
from contouring.parser import Parser

FIXTURE_DIR = os.path.dirname(os.path.realpath(__file__))

@pytest.fixture
def pressure_contours():
    data_file = os.path.join(FIXTURE_DIR, 'pressurecoverage_contours_0-1050.xml')
    with open(data_file, 'r') as f:
        wfs_data = f.read()
    f.closed
    return wfs_data

@pytest.fixture
def windgust_contours():
    data_file = os.path.join(FIXTURE_DIR, 'windgustcoverage_contours_10-25.xml')
    with open(data_file, 'r') as f:
        wfs_data = f.read()
    f.closed
    return wfs_data

@pytest.fixture
def windgust_multi_contours():
    data_file = os.path.join(FIXTURE_DIR, 'windgustcoverage_contours_0-5_5-10_10-15.xml')
    with open(data_file, 'r') as f:
        wfs_data = f.read()
    f.closed
    return wfs_data

def test_pressure(pressure_contours):
    assert type(pressure_contours) is str

def test_windgust(windgust_contours):
    parser = Parser()
    results = parser.parseWFSForecast(windgust_contours)    
    assert type(results) is list
