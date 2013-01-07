# -*- coding:utf-8 -*-

import random
import json
import urllib
from tornado import httpclient
from json import loads as jload


def modal(id, info):
    modal = ''.join([
        '<div id="', id, '" class="modal hide fade" tabindex="-1" '
        'role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">'
        '<div class="modal-header">',
        '<button type="button" class="close" data-dismiss="modal" ',
        'aria-hidden="true">',
        '&times;</button>',
        '</div>',
        '<div class="modal-body" background-color="#eee"><pre>', info,
        '</pre></div>',
        '<div class="modal-footer">',
        '<button class="btn" data-dismiss="modal">Close</button>',
        '</div>',
        '</div>',
    ])
    return modal


def firstmeet():
    firsthello_list = ['Hello', 'Hi']
    firsthello = random.choice(firsthello_list)
    return firsthello


def expression():
    normal = ['~', '~~~']
    normal = random.choice(normal)
    return normal


def hello(usersay):
    hello = ''
    if u'你好' in usersay:
        hello += u'你也好'
    return hello


def song(usersay):
    song = ''
    if u'播放' in usersay:
        song += u'好的~'
        artist = ''
        songname = usersay.split(u'播放')[1]
        if '@@' in songname:
            artist = songname.split('@@')[1]
            songname = songname.split('@@')[0]

        image_url = ''.join([
            'http://api.douban.com/music/subjects?q=',
            urllib.quote(songname.encode('utf-8')),
            '&alt=json&start-index=1&max-results=1',
        ])
        http_client = httpclient.HTTPClient()
        try:
            response = http_client.fetch(image_url)
        except httpclient.HTTPError, e:
            print "Error:", e
        if response.code == 200:
            res = jload(response.body)
            music_image = res['entry'][0]['link'][2]['@href']
            music_image = '<img src="%s" style="float:left"/>' % music_image
            if not artist:
                artist = res['entry'][0]['author'][0]['name']['$t']
            song += music_image

        singer = ''
        if artist:
            singer = '&singer=' + urllib.quote(artist.encode('gbk'))
        lyric_url = ''.join([
            'http://cgi.music.soso.com/fcgi-bin/'
            'fcg_download_lrc.q?song=',
            urllib.quote(songname.encode('gbk')),
            singer,
            '&down=1',
        ])
        print lyric_url
        try:
            response = http_client.fetch(lyric_url)
        except httpclient.HTTPError, e:
            print "Error:", e

        if response.code == 200:
            lyric = response.body.decode('gbk')  # .encode('utf-8')
            lyric_link = ''.join([
                u'<a data-toggle="modal" href="#lyric">',
                u'<span>查看歌词</span></a>',
            ])
            print lyric
            lyric = modal('lyric', lyric)
            lyric_link += lyric
            song += lyric_link

        artist_u = ''
        if artist:
            artist_u = '&amp;artist=' + urllib.quote(artist.encode('utf-8'))
            artist_u = artist_u.replace(']', ']\n')
        songbox = ''.join([
            '<p><embed width="550" height="75" name="plugin" ',
            'wmode="transparent" ',
            'src="http://box.baidu.com/widget/flash/song.swf?name=',
            urllib.quote(songname.encode('utf-8')),
            artist_u,
            '" type="application/x-shockwave-flash"></p>'
        ])
        song += songbox

    return song


def get_ande_ip():
    return urllib.urlopen('http://ifconfig.me/ip').read()


def get_ipinfo(ip):
    if ip == '127.0.0.1':
        ip = get_ande_ip()
    return json.loads(urllib.urlopen(
        'http://ip.taobao.com/service/getIpInfo.php?ip=' + ip).read())


def get_weather(city):
    url = 'http://sou.qq.com/online/get_weather.php?callback=Weather&city='
    city = urllib.quote(city.encode('utf-8'))
    return json.loads(urllib.urlopen(url + city).read()[8:-2])


def weather(usersay, userip):
    weather = ''
    if u'天气' in usersay:
        city = get_ipinfo(userip)['data']['city']
        weather = get_weather(city)
        wea_0 = weather['future']['wea_0']
        tmin_0 = weather['future']['tmin_0']
        tmax_0 = weather['future']['tmax_0']
        wea_1a = weather['future']['forecast'][1]['BWEA']
        wea_1b = weather['future']['forecast'][1]['EWEA']
        tmax_1 = weather['future']['forecast'][1]['TMAX']
        tmin_1 = weather['future']['forecast'][1]['TMIN']
        if wea_1a == wea_1b:
            wea_1 = u'整天%s' % (wea_1a)
        else:
            wea_1 = u'%s转%s' % (wea_1a, wea_1b)
        weather = u'今天天气是%s,%s到%s摄氏度' % (wea_0, tmin_0, tmax_0)
        weather += '<br />'
        weather += u'明天天气是%s,%s到%s摄氏度' % (wea_1, tmin_1, tmax_1)
    return weather
