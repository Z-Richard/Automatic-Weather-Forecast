"""
1. Data from Meteogram URL includes information about all-level (from surface to 150hpa) dew point temperature,
geopotential height, relative humidity (which may be used to compute cloud rate at different levels),
temperature, wind_u and wind_v component.

2. Data from v2.1 URL is more concise and "practical"; it contains only the ground-level data (precipitation,
relative humidity, wind speed, wind direction, gusts, pressure, cloudbase - cbase, sunrise and sunset time,
moon phase, weather icon, weather code) as well as a summary of the predicted weather in the next few days. 

3. Typically (if the ECMWF server is running properly), we will be analyzing 12z data (which starts
from 20:00 at UTC+8, China). 
0 - 23:00, 1 - 2:00, 2 - 5:00, 3 - 8:00, 4 - 11:00, 5 - 14:00
6 - 17:00, 7 - 20:00, 8 - 23:00, 9 - 2:00, 10 - 5:00, 11 - 8:00,
12 - 11:00, 13 - 14:00, 14 - 17:00, 15 - 20:00
We want to focus more on [6:15] (from 17:00 to 17:00 the next day) for deciding the wet_index().

Author: Haoyu Zhuang
Time: April 5, 2020
"""

import urllib.request, urllib.error
import json
import math
import url_const


def request_data(url):
    try:
        data = urllib.request.urlopen(url).read()
        record = data.decode('UTF-8')
        result = json.loads(record)
        return result
    except urllib.error:
        print('We have trouble accessing the windy API. Please contact the programmer for more info.')


def process_dew_data():
    """
    :return: wall_sweating, a number, 0 - no wall-sweating, 1 - slight or moderate, 2 - strong
    dew_point, an array, that presents average dew_point temperature from 8:00 - 17:00 the next day
    """
    data = request_data(url_const.windyUrl)

    dew_point = data['data']['dewPoint'][6:15]
    temperature = data['data']['temp'][6:15]
    wall_sweating = 0
    for d, t in zip(dew_point, temperature):
        if -1 < d - t < 0.5:
            wall_sweating = 1
        elif d - t > 0.5:
            wall_sweating = 2
            break

    return wall_sweating, sum(dew_point[5:]) / len(dew_point[5:])


def process_wind_data():
    """
    900-hpa wind direction coming from 'wind_v-900h' and 'wind_u-900h'
    :return: wind_900_direction, the mode of wind direction in the 17:00 - 17:00 (next day) time range;
    the maximum of 900hpa wind;
    wind_surface_dir, wind direction at 14:00 the next day;
    the maximum of surface wind;
    the maximum of surface gust;
    """
    data = request_data(url_const.meteogramUrl)
    wind_900_v = data['data']['wind_v-900h'][6:15]
    wind_900_u = data['data']['wind_u-900h'][6:15]
    wind_900_direction = [wind_direction((270 - math.atan2(v, u) * 180 / math.pi) % 360)
                          for v, u in zip(wind_900_v, wind_900_u)]
    wind_900 = [math.sqrt(v * v + u * u) for v, u in zip(wind_900_v, wind_900_u)]
    second_data = request_data(url_const.windyUrl)
    wind_surface = second_data['data']['wind'][6:15]
    gust_surface = second_data['data']['gust'][6:15]
    wind_surface_dir = second_data['data']['windDir'][13]

    return max(set(wind_900_direction), key=wind_900_direction.count), float('{0:.3f}'.format(max(wind_900))), \
           wind_surface_dir, max(wind_surface), float('{0:.3f}'.format(max(gust_surface)))


def process_weather_code():
    """
    SKC - no visible clouds
    FEW - 1-2 oktas
    SCT - 3-4 oktas, stand for scatter
    BKN - 5-7 oktas, stand for broken
    OVC - 8 oktas, full cloud coverage
    :return: weather_code that appears most frequently from the 17:00 to 17:00 period
    """
    data = request_data(url_const.windyUrl)
    weather_code = [a.split(',')[0] for a in (data['data']['weathercode'][6:15])]
    return weather_code


def wind_direction(wind_dir):
    if 22.5 < wind_dir <= 67.5:
        result = "东北"
    elif 67.5 < wind_dir <= 112.5:
        result = "东"
    elif 112.5 < wind_dir <= 157.5:
        result = "东南"
    elif 157.5 < wind_dir <= 202.5:
        result = "南"
    elif 202.5 < wind_dir <= 247.5:
        result = "西南"
    elif 247.5 < wind_dir <= 292.5:
        result = "西"
    elif 292.5 < wind_dir <= 327.5:
        result = "西北"
    elif 0 <= wind_dir <= 22.5 or 327.5 < wind_dir <= 360:
        result = "北"
    else:
        result = ""
    return result


if __name__ == '__main__':
    print(process_wind_data())
