"""
The Code Snippet to process the Shenzhen Forecast.

Author: Haoyu Zhuang
Date: April 5, 2020
"""

import urllib.request, urllib.error
import json
import url_const


def request_data(url):
    try:
        headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
        request = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(request).read()
        record = data.decode('UTF-8')
        result = json.loads(record)
        return result
    except urllib.error:
        print('We have trouble accessing the API from SZMB. Please contact the programmer for more info.')


def get_sz_forecast():
    data = request_data(url_const.szForecastUrl)
    forecast = data['data']['forecast10d']['list'][0]
    max_t = forecast['maxt']
    min_t = forecast['mint']
    wind_direction = forecast['wd']
    return min_t, max_t, wind_direction


if __name__ == '__main__':
    print(get_sz_forecast())
