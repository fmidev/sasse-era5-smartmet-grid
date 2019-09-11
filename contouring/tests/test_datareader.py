import pytest
from contouring.datareader import Datareader

def test_datareader_parameters():
    dr = Datareader('localhost')
    assert dr.service_url == 'localhost'
    assert dr.version == '2.0.0'

