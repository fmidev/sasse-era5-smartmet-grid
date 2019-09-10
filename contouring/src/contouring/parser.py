# -*- coding: utf-8 -*-

from owslib.wfs import WebFeatureService
import xml.etree.ElementTree as ET

class Parser(object):

    def parseWFSForecast(self, data):
        """Format XML response to dict

        Returns:
                Dictionary with results from WFS 
                {'timestamp': {'parameter': 'value', 'parameter': 'value'},
                ...
                 'timestamp': {'parameter': 'value', 'parameter': 'value'}}
        """
        root = ET.fromstring(data)
        forecast = {}
        for measurement_timeseries in root.iter('{http://www.opengis.net/waterml/2.0}MeasurementTimeseries'):
            attributes = measurement_timeseries.attrib            
            id = attributes['{http://www.opengis.net/gml/3.2}id'].split('-')[-1]
            # Save parameter values to forecast
            for MeasurementTVP in measurement_timeseries.iter('{http://www.opengis.net/waterml/2.0}MeasurementTVP'):
                if MeasurementTVP[0].text not in forecast:
                    forecast[MeasurementTVP[0].text] = {} 
                forecast[MeasurementTVP[0].text][id] = MeasurementTVP[1].text
        return []