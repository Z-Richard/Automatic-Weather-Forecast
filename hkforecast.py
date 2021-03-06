"""
The Code Snippet to process the HK forecast.

Author: Haoyu Zhuang
Date: April 5, 2020
"""

import urllib.request, urllib.error
import json
import url_const


def request_data(url):
    try:
        data = urllib.request.urlopen(url).read()
        record = data.decode('UTF-8')
        result = json.loads(record)
        return result
    except urllib.error:
        print('We have trouble getting access to HK forecast. Please contact the programmer for more info.')


def get_hk_forecast():
    data = request_data(url_const.hkForecastUrl)
    weather = data['weatherForecast'][0]
    date = weather['forecastDate'][4:6] + '-' + weather['forecastDate'][6:]
    max_t = weather['forecastMaxtemp']['value']
    min_t = weather['forecastMintemp']['value']
    max_rh = weather['forecastMaxrh']['value']
    min_rh = weather['forecastMinrh']['value']
    return date, min_t, max_t, min_rh, max_rh


if __name__ == '__main__':
    print(get_hk_forecast())
