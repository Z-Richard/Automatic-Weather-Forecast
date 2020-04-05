import windy
import windy_rain
import weathernow
import hkforecast
import szforecast

"""
To-do list: 
1. Write the result to an excel file automatically determine the season at the start of the program
so that the user doesn't have to calculate the average temperature in the past 5 days and determine the season. 

2. Train a machine-learning model to predict the maximum and minimum temperature more accurately.
As for now, function maximum_temperature() and minimum_temperature() will not be used. 
"""

min_humidity = {
    "春季": {"SKC": 5, "FEW": 5, "SCT": 0, "BKN": 0, "OVC": 0},
    "夏季": {"SKC": 5, "FEW": 5, "SCT": 0, "BKN": 0, "OVC": 0},
    "秋季": {"SKC": -5, "FEW": -5, "SCT": -10, "BKN": -10, "OVC": -15},
    "冬季": {"SKC": 0, "FEW": 0, "SCT": -10, "BKN": -10, "OVC": -15}
}

max_humidity = {
    "春季": {"SKC": 5, "FEW": 5, "SCT": 0, "BKN": 0, "OVC": 0},
    "夏季": {"SKC": 5, "FEW": 5, "SCT": 0, "BKN": -5, "OVC": -5},
    "秋季": {"SKC": 0, "FEW": 0, "SCT": -10, "BKN": -10, "OVC": -10},
    "冬季": {"SKC": 0, "FEW": 0, "SCT": -10, "BKN": -10, "OVC": -10}
}

star = {
    "SKC": "极好", "FEW": "好", "SCT": "一般", "BKN": "差", "OVC": "极差"
}

cloud_index = {
    "SKC": 4, "FEW": 4, "SCT": 3, "BKN": 3, "OVC": 2
}

insect_value = {
    1: "没有威胁", 2: "敏感人群需防护", 3: "需做简单防护", 4: "需做周到防护", 5: "急需做周到防护"
}

clothing_value = {
    1: "短袖短裤（紧急防暑）", 2: "短袖（注意防暑）", 2.5: "短袖", 3: "单衣或外套", 3.5: "外套", 4: "外套或毛衣",
    4.5: "毛衣或棉袄（防寒）", 5: "棉袄秋裤（紧急防寒）"
}

wet_value = {
    1: "地面干燥", 2: "有少数地方积水", 3: "地面较为湿滑", 4: "地面湿滑（轻微回南天）", 5: "显著回南天"
}

outdoor_value = {
    0: (1, '不适宜'), 1: (2, '较不适宜'), 2: (3, '比较适宜'), 4: (3, '比较适宜'),
    8: (4, '适宜'), 16: (4, '适宜'), 32: (5, '非常适宜')
}

drying_value = {
    1: "需收回衣物", 2: "不适宜晾晒", 3: "晾晒效果较差", 4: "适宜晾晒", 5: "非常适合晾晒"
}


def night_index(c_rate):
    """
    计算观星指数
    :return: 20:00 - star index; 23:00 - star index.
    """
    return star[c_rate[1]], star[c_rate[2]]


def wet_index(light, moderate, heavy, torrential, wall_sweating):
    """
    计算湿滑指数
    :return: a pair of (index, advice)
    """
    if wall_sweating == 1:
        if (light >= 0.5 or moderate >= 0.5 or heavy >= 0.5) and torrential <= 0.5:
            return 4, wet_value[4]
        elif torrential >= 0.5:
            return 5, wet_value[5]
    elif wall_sweating == 2:
        return 5, wet_value[5]
    else:
        if torrential >= 0.5:
            return 4, wet_value[4]
        elif heavy >= 0.5:
            return 3, wet_value[3]
        elif moderate >= 0.5:
            return 2, wet_value[2]
        elif light >= 0.5:
            return 1, wet_value[1]


def drying_index(gust, wet, c_season, c_rate, rh, wind, maximum_t):
    """
    计算晾晒指数
    :return: a pair of (index, advice)
    """
    y = 43.547 + 0.2 * maximum_t - 0.8 * rh + 0.5 * wind + 1.6 * cloud_index[c_rate]
    if gust >= 12.0 or wet == 5:
        return 1, drying_value[1]
    elif wet == 4:
        return 2, drying_value[2]
    elif c_season == "春季" or "夏季":
        if y <= -5.0:
            return 3, drying_value[3]
        elif y <= 0.0:
            return 4, drying_value[4]
        else:
            return 5, drying_value[5]
    elif c_season == "秋季" or "冬季":
        if y <= 3.0:
            return 3, drying_value[3]
        elif y <= 8.0:
            return 4, drying_value[4]
        else:
            return 5, drying_value[5]


def outdoor_index(c_rate, light, moderate, net_value, dew_point, wind, pollution):
    """
    计算运动指数
    :return: a pair of (index, advice)
    """
    if moderate >= 0.5:
        a = 0
    elif c_rate == "SKC" or (moderate < 0.5 < light):
        a = 1
    elif c_rate != "SKC" and light <= 0.5:
        a = 2

    if net_value >= 26.63 or net_value <= 3.70:
        b = 0
    elif net_value >= 24.07 or net_value <= 13.22:
        b = 1
    else:
        b = 2

    if dew_point >= 25.0:
        c = 0
    elif dew_point >= 22.0:
        c = 1
    else:
        c = 2

    if wind >= 12.0:
        d = 0
    elif wind >= 9.0:
        d = 1
    else:
        d = 2

    if pollution >= 150:
        e = 0
    elif pollution >= 75:
        e = 1
    else:
        e = 2

    return outdoor_value[a * b * c * d * e]


def clothing_index(net_value):
    """
    计算穿衣指数
    :return: a pair of (index, advice)
    """
    if net_value >= 27.38:
        return 1, clothing_value[1]
    elif net_value >= 26.63:
        return 2, clothing_value[2]
    elif net_value >= 24.07:
        return 2.5, clothing_value[2.5]
    elif net_value >= 18.00:
        return 3, clothing_value[3]
    elif net_value > 13.22:
        return 3.5, clothing_value[3.5]
    elif 3.70 < net_value <= 13.22:
        return 4, clothing_value[4]
    elif 0.63 < net_value <= 3.70:
        return 4.5, clothing_value[4.5]
    return 5, clothing_value[5]


def insect_index(c_season, minimum_t, maximum_rh):
    """
    计算蚊虫指数
    :return: a pair of (index, advice)
    """
    if c_season == "冬季":
        return 1, insect_value[1]
    raw_score = -24 + 0.2 * minimum_t + 0.3 * maximum_rh
    if raw_score <= 0:
        return 1, insect_value[1]
    elif 0 < raw_score <= 5:
        return 2, insect_value[2]
    elif 5 < raw_score <= 8:
        return 3, insect_value[3]
    elif 8 < raw_score <= 9.5:
        return 4, insect_value[4]
    return 5, insect_value[5]


def rain_probability(r_sequence):
    """
    计算降水概率
    r_sequence, rain sequence, a list with 10 items. See windy_rain.py for more info.
    :return: the probability for light rain, moderate rain, heavy rain, and torrential rain
    """
    return len([a for a in r_sequence if a > 1]) / len(r_sequence), \
           len([b for b in r_sequence if b > 10]) / len(r_sequence), \
           len([c for c in r_sequence if c > 25]) / len(r_sequence), \
           len([d for d in r_sequence if d > 50]) / len(r_sequence)


def max_min_humidity(minimum, maximum, c_season, c_rate):
    """
    修正湿度
    maximum & minimum - forecast humidity by HKO
    c_season, current season
    c_rate, cloud rate, represented by "SKC", "FEW", "SCT", "BKN", "OVC"
    :return: modified_maximum_humidity, modified_minimum_humidity
    """
    return minimum + min_humidity[c_season][c_rate], maximum + max_humidity[c_season][c_rate]


def net(t, rh, v):
    """
    计算有效气温
    :return: net_value, a measurement of "real feel" : how cold or hot it is now.
    """
    return 37 - ((37 - t) / (0.68 - 0.0014 * rh + 1 / (1.76 + 1.4 * pow(v, 0.75)))) - 0.29 * t * (1 - 0.01 * rh)


def maximum_temperature():
    """
    修正最高气温
    :return:
    """
    return


def minimum_temperature():
    """
    修正最低气温
    :return:
    """
    return


if __name__ == '__main__':
    season = input('请输入现在的季节：')
    air_quality = int(input('请输入预期的AQI值：'))

    weather_code = windy.process_weather_code()
    wind_900_dir, wind_900_max, wind_surface_dir, wind_surface_max, gust_surface_max = windy.process_wind_data()
    cloud_rate = max(set(weather_code), key=weather_code.count)
    date, min_t, max_t, min_rh, max_rh = hkforecast.get_hk_forecast()
    mod_min_rh, mod_max_rh = max_min_humidity(min_rh, max_rh, season, cloud_rate)
    print('修正后的最低湿度：', mod_min_rh, '\n', '修正后的最高湿度：', mod_max_rh, sep="")

    max_day_t, min_day_t, max_wind, max_gust, rain = weathernow.get_weather_now()
    print('今日最低气温：', min_day_t, '\n', '今日最高气温：', max_day_t, '\n', '最大风速：', max_wind, '\n',
          "极大风速：", max_gust, '\n', '24小时降水：', rain, sep="")

    net = float('{0:.3f}'.format(net((min_t + max_t) / 2, (mod_min_rh + mod_max_rh) / 2, wind_surface_max)))
    print('Net指数为：', net, sep="")

    rain = windy_rain.compute_rain()
    light_rain, moderate_rain, heavy_rain, torrential_rain = rain_probability(rain)
    print("小雨，中雨，大雨，暴雨可能性", light_rain, moderate_rain, heavy_rain, torrential_rain)

    wall_sweat, dew = windy.process_dew_data()
    print("回南天指数", wall_sweat)

    insect_ind, insect_desc = insect_index(season, min_t, mod_max_rh)
    print("蚊虫指数", insect_ind, insect_desc)

    wet_ind, wet_desc = wet_index(light_rain, moderate_rain, heavy_rain, torrential_rain, wall_sweat)
    print("湿滑指数", wet_ind, wet_desc)

    outdoor_ind, outdoor_desc = outdoor_index(cloud_rate, light_rain, moderate_rain, net,
                                              dew, gust_surface_max, air_quality)
    print("运动指数", outdoor_ind, outdoor_desc)

    drying_ind, drying_desc = drying_index(gust_surface_max, wet_ind, season, cloud_rate,
                                           (mod_max_rh + mod_min_rh) / 2, wind_surface_max, max_t)
    print("晾晒指数", drying_ind, drying_desc)

    clothing_ind, clothing_desc = clothing_index(net)
    print("穿衣指导", clothing_ind, clothing_desc)

    star_start, star_end = night_index(weather_code)
    print("观星指数\n20：00起", star_start, "23：00起", star_end)
