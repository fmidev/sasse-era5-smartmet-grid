# -*- coding: utf-8 -*-

from owslib.wfs import WebFeatureService
import xml.etree.ElementTree as ET

class Datareader(object):
    """Employee class is used to hold employee object data.
 
    Methods:
        __init__(self, emp_id, emp_name)
        print()
    """

    def __init__(self, service_url='http://smartmet.fmi.fi/wfs', wfs_version='2.0.0'):
        self.service_url = service_url
        self.version = wfs_version

    def _getForecastDataValidTime(self):
        """Read latest Harmonie data begin time and end time

            Return:
                tuple of starttime and endtime 
        """
        storedquery_id = 'fmi::forecast::harmonie::surface::grid'
        wfs_query = WebFeatureService(url=self.service_url, version=self.version)
        response = wfs_query.getfeature(storedQueryID=storedquery_id, storedQueryParams={})
        root = ET.parse(response).getroot()
        for child in root.iter('{http://www.opengis.net/om/2.0}validTime'):
            for i in child.iter('{http://www.opengis.net/gml/3.2}beginPosition'):
                beginPosition = i.text
            for i in child.iter('{http://www.opengis.net/gml/3.2}endPosition'):
                endPosition = i.text
        return (beginPosition, endPosition)

    def _parseWFSForecast(self, response):
        """Format XML response to dict

        Returns:
                Dictionary with results from WFS 
                {'timestamp': {'parameter': 'value', 'parameter': 'value'},
                ...
                 'timestamp': {'parameter': 'value', 'parameter': 'value'}}
        """
        root = ET.parse(response).getroot()
        forecast = {}
        for measurement_timeseries in root.iter('{http://www.opengis.net/waterml/2.0}MeasurementTimeseries'):
            attributes = measurement_timeseries.attrib            
            id = attributes['{http://www.opengis.net/gml/3.2}id'].split('-')[-1]
            # Save parameter values to forecast
            for MeasurementTVP in measurement_timeseries.iter('{http://www.opengis.net/waterml/2.0}MeasurementTVP'):
                if MeasurementTVP[0].text not in forecast:
                    forecast[MeasurementTVP[0].text] = {} 
                forecast[MeasurementTVP[0].text][id] = MeasurementTVP[1].text
        return forecast

    def getWindForecast(self, latitude, longitude, height):
        """Get latest wind speed forecast for given location

            Args:
                latitude: Target location degrees latitude
                longitude: Target location degrees longitude
                height: Target location height in meters (hub height)
            Returns:
                Dictionary with results from WFS 
                {'timestamp': {'parameter': 'value', 'parameter': 'value'},
                ...
                 'timestamp': {'parameter': 'value', 'parameter': 'value'}}
        """
        starttime, endtime = self._getForecastDataValidTime()
        if (height < 13):
            height = 13
        if (height > 10000):
            height = 10000
        storedquery_id = 'fmi::forecast::harmonie::hybrid::point::timevaluepair'
        parameters = ('WindSpeedMs', 'WindDirection', 'Pressure')
        wfs_query = WebFeatureService(url=self.service_url, version=self.version)
        stored_query_params = {
            'latlon': '{0},{1}'.format(latitude, longitude),
            'parameters': ','.join(parameters),
            'height': height,
            'starttime': starttime,
            'endtime': endtime
        }
        response = wfs_query.getfeature(storedQueryID=storedquery_id, storedQueryParams=stored_query_params)
        forecast = self._parseWFSForecast(response)
        return forecast

    def getRadiationGlobalFractilesForecast(self, latitude, longitude, starttime, endtime):
        """Get forecast for F0-F100 for Global Radiation WFS

            Args:
                latitude: Target location degrees latitude
                longitude: Target location degrees longitude
                starttime: First available timestep in forecast
                endtime: Last available timestep in forecast
            Returns:
                Dictionary with results from WFS 
                {'timestamp': {'parameter': 'value', 'parameter': 'value'},
                ...
                 'timestamp': {'parameter': 'value', 'parameter': 'value'}}
        """
        storedquery_id = 'fmi::forecast::harmonie::surface::fractile::point::timevaluepair'
        # parameters = ('4678', '4677', '4676', '4675', '4674', '4673', '4672')
        parameters = ('RadiationGlobalF100', 'RadiationGlobalF90', 'RadiationGlobalF75', 'RadiationGlobalF50', 'RadiationGlobalF25', 'RadiationGlobalF10', 'RadiationGlobalF0')

        wfs_query = WebFeatureService(url=self.service_url, version=self.version)
        stored_query_params = {
            'latlon': '{0},{1}'.format(latitude, longitude),
            'parameters': ','.join(parameters),
            'starttime': starttime,
            'endtime': endtime
        }
        response = wfs_query.getfeature(storedQueryID=storedquery_id, storedQueryParams=stored_query_params)
        forecast = self._parseWFSForecast(response)
        return forecast

def main():
    dr = Datareader()
    latitude = 60.19206
    longitude = 24.94583
    height = 50000
    response = dr.getWindForecast(latitude, longitude, height)
    print(response)
    latitude = 60.203561
    longitude = 24.961179
    starttime = "2018-09-27T05:00:00Z"
    endtime = "2018-09-29T21:00:00Z"
    print(dr.getRadiationGlobalFractilesForecast(latitude, longitude, starttime, endtime))

if __name__ == '__main__':
    main()