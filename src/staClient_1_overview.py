# -*- coding: UTF-8 -*-
#staClient_1_overview.py
from __future__ import absolute_import, division, print_function, unicode_literals
import requests
import json
import sys

def requestCountClass(staClassUrl: str, proxies: dict) -> int:
    """Methode requestCountClass gibt die Anzahl der Objekte der uebergebenen Klasse zurueck.
    
    Args:
        staClassUrl: str with url sta class
        proxies: dict with proxies
        
    Returns:
        int with count objects sta class
        
    Raises:
        ConnectionError for Service is down
    """
    jsonData = None
    url = '%s%s' % (staClassUrl, '?$top=1&$count=true')
    r = requests.get(url, proxies=proxies)
    
    if r.status_code == 200:
        jsonData = json.loads(r.text)
    else:
        message = '%s: %s' % (r.status_code, 'Service is down')
        raise ConnectionError(message)
    
    return jsonData['@iot.count']
    
def main():
    """Ueberblick ueber die Klassen der SensorThings API (STA).
    
    1. Welche Klassen.
    2. Count je Klasse.
    3. Wieviele und Welche Things gibt es, wie sind sie rauemlich verteilt:
        FME Workbench staThings.fmw (verbraucht viel temporaeren Festplattenspeicher auf AppData\Local\Temp)
    """
    proxies = {
        'http': 'http://111.11.111.111:80',
        'https': 'http://111.11.111.111:80',
        }
    
    urlStaApi = 'https://iot.hamburg.de/v1.1'
    
    #1. Welche Klassen
    jsonData = None
    r = requests.get(urlStaApi, proxies=proxies)
    print('Klassen der STA %s:' % (urlStaApi))
    print('###############')
    
    if r.status_code == 200:
        jsonData = json.loads(r.text)
        
        for element in jsonData['value']:
            try:
                count = requestCountClass(element['url'], proxies)
                print('{%s: %s}, {count: %s}' % (element['name'], element['url'], count))
            except ConnectionError:
                print('%s; %s' % (sys.exc_info()[0], sys.exc_info()[1]))
    else:
        print('%s: %s' % (r.status_code, 'Service is down'))
        sys.exit()
              
if __name__ == '__main__':
    main()
	