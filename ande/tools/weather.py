#!/usr/bin/env python
#-*-coding:utf-8-*-

"""
Copyright (c) 2013 Qimin Huang <qiminis0801@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# 天气
import os
import json
import requests
import cPickle as pickle
import ip
import urllib


def test(data):
    return u'天气' in data['usersay']


def weather0(cityid):
    url = 'http://www.weather.com.cn/data/cityinfo/%s.html' % cityid
    weatherinfo = requests.get(url).json()['weatherinfo']
    weather = ''.join([
        '', weatherinfo['city'],
        ', ', weatherinfo['weather'],
        ', ', weatherinfo['temp1'],
        ' ~ ', weatherinfo['temp2'],
    ]).encode('utf8')
    return weather


def weather1(city):
    if city:
        weather = ''
        url = 'http://sou.qq.com/online/get_weather.php?callback=Weather&city='
        city = urllib.quote(city.encode('utf-8'))
        weather = json.loads(urllib.urlopen(url + city).read()[8:-2])
        wea_0 = weather['future']['wea_0']
        tmin_0 = weather['future']['tmin_0']
        tmax_0 = weather['future']['tmax_0']
        wea_1a = weather['future']['forecast'][1]['BWEA']
        wea_1b = weather['future']['forecast'][1]['EWEA']
        tmax_1 = weather['future']['forecast'][1]['TMAX']
        tmin_1 = weather['future']['forecast'][1]['TMIN']
        if wea_1a == wea_1b:
            wea_1 = u'整天%s' % wea_1a
        else:
            wea_1 = u'%s转%s' % (wea_1a, wea_1b)
        weather = u'今天天气是%s,%s到%s摄氏度' % (wea_0, tmin_0, tmax_0)
        weather += '\n'
        weather += u'明天天气是%s,%s到%s摄氏度' % (wea_1, tmin_1, tmax_1)
        return weather
    else:
        return 'I don\'t know'


def city(usersay):
    cityidDict = pickle.load(file(os.path.join(
        os.path.dirname(__file__), 'data' + os.path.sep + 'cityid'), 'r'))
    for i in cityidDict:
        # if i.encode('utf8') in usersay:
        if i in usersay:
            return i, cityidDict[i]
    return '', ''


def handle(data):
    if city(data['usersay']):
        cityname, cityid = city(data['usersay'])
    else:
        if 'userip' in data:
            cityname = ip.get_ipinfo(data['userip'])['data']['city']
            cityname = cityname.encode('utf8')
            cityname, cityid = city(cityname)
        else:
            return 'I don\'t know'
    return weather1(cityname)
    # return weather0(cityid)

if __name__ == '__main__':
    datas = [
        {'usersay': u'今天天气怎么样'},
        {'usersay': u'天气怎么样', 'userip': '127.0.0.1'},
        {'usersay': u'武汉天气怎么样'},
        {'usersay': u'武汉天气怎么样'},
        {'usersay': u'北京天气怎么样'},
    ]
    for data in datas:
        print(data['usersay'], test(data), handle(data))
