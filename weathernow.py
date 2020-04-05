import urllib.request, urllib.error
import json

url = 'http://data.121.com.cn/szmbdata/open/openData.do?type=17&' \
      'appid=1550582904725&appKey=bb351c34-3c61-4174-b55b-e9c833a10567'


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


def get_weather_now():
    data = request_data(url)
    sfls_data = [a for a in data['data'] if a['name'] == '明珠'][0]
    day_max_t = sfls_data['maxtday']
    day_min_t = sfls_data['mintday']
    day_max_wind = sfls_data['wd10maxdfday']
    day_max_gust = sfls_data['wd3smaxdfday']
    rain_24h = sfls_data['r24h']
    return day_max_t, day_min_t, day_max_wind, day_max_gust, rain_24h


if __name__ == '__main__':
    print(get_weather_now())
