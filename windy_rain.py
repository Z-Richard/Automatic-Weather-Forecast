import urllib.request, urllib.error
import json
import random

lat = 22.580
lon = 114.247
url = 'https://node.windy.com/forecast/v2.1/ecmwf/'
lat_lon_range = [[0.25, 0.75], [-0.25, 0.25], [-0.75, -0.25]]


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
    for _lat in lat_lon_range:
        for _lon in lat_lon_range:
            a = [float('{0:.3f}'.format(random.uniform(lat + _lat[0], lat + _lat[1]))) for i in range(10)]
            b = [float('{0:.3f}'.format(random.uniform(lon + _lon[0], lon + _lon[1]))) for i in range(10)]
            pre_rain = []
            for elem in list(zip(a, b)):
                data = request_data(url + str(elem[0]) + '/' + str(elem[1]))
                pre_rain.append(sum(data['data']['mm'][5:13]))
            spec_rain.append(float('{0:.2f}'.format(sum(pre_rain) / len(pre_rain))))
    sfls_data = request_data(url + str(lat) + '/' + str(lon))
    spec_rain.append(float('{0:.2f}'.format(sum(sfls_data['data']['mm'][5:13]))))

    return spec_rain


if __name__ == '__main__':
    print(compute_rain())
