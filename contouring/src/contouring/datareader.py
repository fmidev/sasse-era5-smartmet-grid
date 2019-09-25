# -*- coding: utf-8 -*-

from owslib.wfs import WebFeatureService
import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from types import SimpleNamespace


def starttimes(start_year: int, start_month: int) -> datetime:
    """Generator for wfs-requests start times for given month.

    Starting from first day of the month at 00:00, 
    incrementing the time with one hour a time so that next time
    would be at 01:00. The iteration will end on last day of the 
    month at 23:00.

    Args:
        start_year: Integer describing targeted year
        start_month: Integer describing targeted month.

    Yields:
        A datetime object starting from first day of given month 
        and ending to the last day and hour .
    """
    next_time = datetime(start_year, start_month, day=1, tzinfo=timezone.utc)
    # month = my_time.month
    while next_time.month == start_month:
        yield next_time
        next_time = next_time + timedelta(hours=1)


class Datareader(object):
    """Working between wfs-server and python"""
 
    def __init__(
        self, 
        wfs_service_url='http://smarmet.fmi.fi/wfs', 
        wfs_version='2.0.0',
        timeout=240
    ):
        self.wfs = WebFeatureService(url=wfs_service_url, version=wfs_version, timeout=timeout)
        self.stored_query_id = None
        self.stored_query_params = SimpleNamespace()

    def getWFS(self):
        """Get latest wind speed forecast for given location
        """
        if not (self.stored_query_id and self.stored_query_params):
            raise AttributeError("Missing id of params for stored query")
        response = self.wfs.getfeature(
            storedQueryID=self.stored_query_id,
            storedQueryParams=vars(self.stored_query_params)
            )
        return response
