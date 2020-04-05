"""
The Code Snippet to process the Windy Rain data.

Author: Haoyu Zhuang
Date: April 5, 2020
"""

import urllib.request, urllib.error
import json
import random
import url_const
import const


def request_data(url):
    try:
        data = urllib.request.urlopen(url).read()
        record = data.decode('UTF-8')
        result = json.loads(record)
        return result
    except urllib.error:
        print('We have trouble accessing the windy API. Please contact the programmer for more info.')


def compute_rain():
    """
    :return: A list of rainfall data using 3 * 3 grid
    And one critical point (22.580, 114.247) within the next 24 hours, i.e. 14:00 - 14:00
    """
    spec_rain = []
    for _lat in const.lat_lon_range:
        for _lon in const.lat_lon_range:
            a = [float('{0:.3f}'.format(random.uniform(const.lat + _lat[0], const.lat + _lat[1]))) for i in range(10)]
            b = [float('{0:.3f}'.format(random.uniform(const.lon + _lon[0], const.lon + _lon[1]))) for i in range(10)]
            pre_rain = []
            for elem in list(zip(a, b)):
                data = request_data(url_const.windyUrl + str(elem[0]) + '/' + str(elem[1]))
                pre_rain.append(sum(data['data']['mm'][5:13]))
            spec_rain.append(float('{0:.2f}'.format(sum(pre_rain) / len(pre_rain))))
    sfls_data = request_data(url_const.windyUrl + str(const.lat) + '/' + str(const.lon))
    spec_rain.append(float('{0:.2f}'.format(sum(sfls_data['data']['mm'][5:13]))))

    return spec_rain


if __name__ == '__main__':
    print(compute_rain())
