# -*- coding: utf-8 -*-

from owslib.wfs import WebFeatureService
import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import timedelta
from datetime import timezone


class Datareader(object):
    """Working between wfs-server and python"""

    def __init__(self, wfs_service_url='http://smartmet.fmi.fi/wfs', wfs_version='2.0.0'):
        self.service_url = wfs_service_url
        self.version = wfs_version

    def starttimes(self, year, month):
        """Generator for wfs-requests start times for given month.

        Starting from first day of the month at 00:00, 
        incrementing the time with one hour a time so that next time
        would be at 01:00. The iteration will end on last day of the 
        month at 23:00.

        Args:
            year: Four digit string describing targeted year
            month: Two digit string describing targeted month.
 
        Yields:
            A datetime object starting from first day of given month 
            and ending to the last day and hour .
        """
        # isostring = f"{self.year}-{self.month}-01 00:00:00+0000"
        # mytime = datetime.strptime(isostring, "%Y-%m-%d %H:%M:%S%z")
        mytime = datetime(year, month, day=1, tzinfo=timezone.utc)
        month = mytime.month
        while mytime.month == month:
            yield mytime
            mytime = mytime + timedelta(hours=1)

    def getWFS(self, storedquery_id, stored_query_params):
        """Get latest wind speed forecast for given location
        """
        wfs_query = WebFeatureService(url=self.service_url, version=self.version)
        response = wfs_query.getfeature(
            storedQueryID=storedquery_id,
            storedQueryParams=stored_query_params
            )
        return response

