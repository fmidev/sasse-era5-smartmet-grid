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
    parser = Parser()
    results = parser.list_contours_in_wfs(pressure_contours)    
    assert type(results) is list
    assert type(results[0]) is dict
    assert results[0]['point_in_time'] == '2017-08-01T00:00:00Z'
    assert 'coordinates' in results[0]
    assert results[0]['weather_parameter'] == 'Pressure'
    assert results[0]['coordinates'].startswith('60.000000 21.000000,63.996000 21.000000')

def test_windgust(windgust_contours):
    parser = Parser()
    results = parser.list_contours_in_wfs(windgust_contours)
    assert type(results) is list
    assert type(results[0]) is dict
    assert results[0]['point_in_time'] == '2017-08-01T00:00:00Z'
    assert 'coordinates' in results[0]
    assert results[0]['weather_parameter'] == 'WindGust'
    assert results[0]['coordinates'].startswith('60.105139 21.000000,63.504664 21.000000')
    assert results[1]['coordinates'].startswith('60.000000 21.716810,60.000088 21.716934')

def test_windgust_multi(windgust_multi_contours):
    parser = Parser()
    results = parser.list_contours_in_wfs(windgust_multi_contours)    
    assert type(results) is list
    assert type(results[0]) is dict
    assert results[0]['point_in_time'] == '2017-08-01T00:00:00Z'
    assert 'coordinates' in results[0]
    assert results[0]['weather_parameter'] == 'WindGust'
    assert results[0]['low_limit'] == '0'
    assert results[1]['low_limit'] == '5'
    assert results[2]['low_limit'] == '5'
    assert results[0]['coordinates'].startswith('60.000000 21.000000,60.105139 21.000000')
    assert results[1]['coordinates'].startswith('60.105139 21.000000,63.504664 21.000000')
    assert results[2]['coordinates'].startswith('60.000000 21.716810,60.000088 21.716934')
