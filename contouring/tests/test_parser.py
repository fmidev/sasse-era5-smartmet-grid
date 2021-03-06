import pytest
import os
from contouring.parser import Parser
import datetime
from sqlalchemy import Column, DateTime, Integer, String

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

def test_parsed_time_fits_orm(pressure_contours):
    parser = Parser()
    results = parser.list_contours_in_wfs(pressure_contours)
    assert type(results[0]['point_in_time']) is Column(DateTime).type.python_type


def test_parsed_limits_fit_orm(pressure_contours):
    parser = Parser()
    results = parser.list_contours_in_wfs(pressure_contours)
    assert type(results[0]['low_limit']) is Column(Integer).type.python_type
    assert type(results[0]['high_limit']) is Column(Integer).type.python_type

# def test_orm_types_datetime(pressure_contours):
#     parser = Parser()
#     results = parser.list_contours_in_wfs(pressure_contours)
    # assert type(results[0]['weather_parameter']) is Column(String).type.python_type

# def test_orm_types_datetime(pressure_contours):
#     parser = Parser()
#     results = parser.list_contours_in_wfs(pressure_contours)
    # assert type(results[0]['unit']) is Column(String).type.python_type
    # Geometry from geoalchemy2 has no python_type implemented, so it is not tested here

def test_pressure(pressure_contours):
    parser = Parser()
    results = parser.list_contours_in_wfs(pressure_contours)    
    assert type(results) is list
    assert type(results[0]) is dict
    # assert results[0]['point_in_time'] == '2017-08-01T00:00:00Z'
    assert datetime.datetime.strftime(results[0]['point_in_time'], "%Y-%m-%dT%H:%M:%SZ") == '2017-08-01T00:00:00Z'
    assert results[0]['weather_parameter'] == 'Pressure'
    assert 'geometry' in results[0]
    assert results[0]['geometry'].startswith('POLYGON((21.000000 60.000000,21.000000 63.996000,')

def test_windgust(windgust_contours):
    parser = Parser()
    results = parser.list_contours_in_wfs(windgust_contours)
    assert type(results) is list
    assert type(results[0]) is dict
    assert datetime.datetime.strftime(results[0]['point_in_time'], "%Y-%m-%dT%H:%M:%SZ") == '2017-08-01T00:00:00Z'
    assert results[0]['weather_parameter'] == 'WindGust'
    assert 'geometry' in results[0]
    assert results[0]['geometry'].startswith('POLYGON((21.000000 60.105139,21.000000 63.504664,')
    assert results[1]['geometry'].startswith('POLYGON((21.716810 60.000000,21.716934 60.000088,')
    assert results[1]['geometry'].endswith(',22.400783 60.000000,21.716810 60.000000))')

def test_windgust_multi(windgust_multi_contours):
    parser = Parser()
    results = parser.list_contours_in_wfs(windgust_multi_contours)    
    assert type(results) is list
    assert len(results) == 3
    
    assert datetime.datetime.strftime(results[0]['point_in_time'], "%Y-%m-%dT%H:%M:%SZ") == '2017-08-01T00:00:00Z'
    assert results[0]['point_in_time'] == results[1]['point_in_time']
    assert results[1]['point_in_time'] == results[2]['point_in_time']
    
    assert results[0]['low_limit'] == 0
    assert results[0]['high_limit'] == 5
    assert results[1]['low_limit'] == 5
    assert results[1]['high_limit'] == 10
    assert results[2]['low_limit'] == results[1]['low_limit']
    
    assert 'geometry' in results[0]
    assert 'geometry' in results[1]
    assert 'geometry' in results[2]

    assert results[0]['geometry'].startswith('POLYGON((21.000000 60.000000,21.000000 60.105139,')
    assert results[1]['geometry'].startswith('POLYGON((21.000000 60.105139,21.000000 63.504664,')
    assert results[2]['geometry'].startswith('POLYGON((21.716810 60.000000,21.716934 60.000088,')
    assert results[2]['geometry'].endswith(',22.400783 60.000000,21.716810 60.000000))')
