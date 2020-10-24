# -*- coding: UTF-8 -*-
#staClient_2_observations.py
from __future__ import absolute_import, division, print_function, unicode_literals
import requests
import json
import sys
import pandas as pd
import matplotlib.pyplot as plt

def main():
    """Wir holen uns alle Observations fuer https://iot.hamburg.de/v1.1/Things(5576)
    fuer den 1 Tag Intervall und plotten sie in einem Line Chart.
    """
    proxies = {
        'http': 'http://111.11.111.111:80',
        'https': 'http://111.11.111.111:80',
        }
    
    urlStaApi = 'https://iot.hamburg.de/v1.1/Datastreams(11846)/Observations'    
    zaehler = 0; count = 100; skip = 100
    resultDict = {}
    
    while zaehler < count:   
        jsonData = None
        url = '%s%s%s' % (urlStaApi, '?$orderBy=phenomenonTime asc&$count=true&$top=100&$skip=', zaehler)
        r = requests.get(url, proxies=proxies)
        
        if r.status_code == 200:
            jsonData = json.loads(r.text)
            count = jsonData['@iot.count']
            zaehler += skip
            
            for o in jsonData['value']:
                ##row = '%s;%s;%s' % (o['phenomenonTime'], o['resultTime'], o['result'])
                #print(row)
                tmpTime = o['phenomenonTime'].split('T')[0]
                resultDict.update({tmpTime: o['result']})
        else:
            print('%s: %s' % (r.status_code, 'Service is down'))
            sys.exit()
            
    s = pd.Series(resultDict)
    s.name = 'Observations:' + urlStaApi
    s.plot.line()
    plt.title('Observations 1Tag Intervall')
    plt.ylabel('Fahrradaufkommen (Anzahl)')
    plt.xlabel('Zeitintervall (Tag)')
    plt.legend()
    plt.show()
    
if __name__ == '__main__':
    main()
	