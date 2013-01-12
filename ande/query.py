# -*- coding:utf-8 -*-

import random
import json
import urllib
from tornado import httpclient
from json import loads as jload
from tools.bingtrans import translate
from db import Ande

hellos = [u'你好', 'hello', 'hi']
e_happys = [':)', '^_^', 'O(∩_∩)O', '(◕‿‿◕)']


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


def firstface():
    firsthello_list = ['Hello', 'Hi']
    firsthello = random.choice(firsthello_list)
    return firsthello


def expression():
    normal = ['~', '~~~']
    normal = random.choice(normal)
    return normal


def is_firstmeet(userip, user_id):
    if user_id == 0:
        a = 'not good friend'
        num = Ande.by_ip(userip)
    else:
        a = 'is good friend'
        num = Ande.by_uid(user_id)
    is_firstmeet = '%s we say %s times' % (a, num)
    return is_firstmeet


def first(usersay, userip, user_id, method):
    first = ''
    if method == 'get' and usersay == '':
        first = hello('hi')
    if method == 'post' and usersay == '':
        first = say_sth()
    return first


def say_sth():
    sths = ['hi~ why not say sth?', 'you seem to test me']
    say_sth = random.choice(sths)
    return say_sth


def hello(usersay):
    hello = ''
    for i in hellos:
        if usersay.startswith(i):
            sayhello = random.choice(hellos)
            e_happy = random.choice(e_happys)
            hello = sayhello + e_happy
    return hello


def clock(usersay):
    times = [u'时间', u'几点', u'几号', u'日期', 'time', 'date']
    clock = ''
    for i in times:
        if i in usersay:
            clock = ''.join([
                u'现在时间是：<span id="clock"></span>',
                '<script type="text/javascript">',
                'var clock = new Clock();',
                'clock.display(document.getElementById("clock"));',
                '</script>',
            ])
    return clock


def song(usersay):
    song = ''
    songhint = [u'播放', u'我想听', 'play:']
    for i in songhint:
        if i in usersay:
            song += u'好的~'
            artist = ''
            songname = usersay.split(i)[1]
            if '@@' in songname:
                songname, artist = songname.split('@@')
            music_image, lyric_link, songbox = get_song(songname, artist)
            song = '%s%s%s%s' % (song, music_image, lyric_link, songbox)
    return song


def get_song(songname, artist):
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
            lyric = modal('lyric', lyric)
            lyric_link += lyric

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
        return music_image, lyric_link, songbox


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


def trans(usersay, userlang):
    trans = ''
    songhint = [u'翻译', u'fanyi：', 't:', 't ']
    for i in songhint:
        if i in usersay:
            trans += u'好的~'
            text = usersay.split(i)[1]
            to = 'en'
            if is_en(text):
                to = userlang
            trans = translate(text, '', to)
    return trans

# def is_cn(i):
#     return 0x4e00 <= ord(i) < 0x9fa6


# def is_en(i):
#     return ord(i) < 128


def is_en(i):
    c = i.encode('utf-8')
    return True if len(c) == len(i) else False
