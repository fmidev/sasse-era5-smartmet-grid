# -*- coding: utf-8 -*-

from owslib.wfs import WebFeatureService
import xml.etree.ElementTree as ET
import datetime

class Parser(object):

    # Namespace definitions for parsing the WFS responses from FMI 
    ns = {
        'wfs' : 'http://www.opengis.net/wfs/2.0',
        'gml' : 'http://www.opengis.net/gml/3.2',
        'om' : 'http://www.opengis.net/om/2.0',
        'omso' : 'http://inspire.ec.europa.eu/schemas/omso/3.0',
        'sam' : 'http://www.opengis.net/sampling/2.0',
        'sams' : 'http://www.opengis.net/samplingSpatial/2.0',
        'fmicov' : 'http://xml.fmi.fi/namespace/weather/2015/09/18/coverages',
        'xlink' : 'http://www.w3.org/1999/xlink',
        'xsi' : 'http://www.w3.org/2001/XMLSchema-instance',
    }

    def list_contours_in_wfs(self, data):
        """Format XML response to list of dictionaries
        
        For each area there can be several surface members with coordinates

        Returns: list of dictionaries
            [{
                'geometry': '',
                'high_limit': '',
                'low_limit': '',
                'point_in_time': '',
                'unit': '',
                'weather_parameter': ''
            },
            ... 
            ]
        """
        root = ET.fromstring(data)
        results = []
        for area in root.findall('.//fmicov:phenomenonArea', self.ns):
            
            for surface in area.findall('.//gml:surfaceMember', self.ns):
                coordinates = surface.findall(
                    './/gml:coordinates', self.ns
                    )[0].text
                results.append({
                    'point_in_time': datetime.datetime.strptime(
                        area.get('dateTime'),
                        "%Y-%m-%dT%H:%M:%SZ"
                        ).replace(tzinfo=datetime.timezone.utc),
                    'weather_parameter': area.get('parameter'),
                    'unit': area.get('unit'),
                    'low_limit': int(area.get('low')),
                    'high_limit': int(area.get('high')),
                    'geometry': f"POLYGON(({coordinates}))"
                })
        return results