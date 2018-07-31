# -*- coding:utf-8 -*-

import random
import urllib
from tornado import httpclient
from json import loads as jload
from pymongo import DESCENDING  # ASCENDING
from db import Ande
from ande.tool.bingtrans import translate
from ande.tool.g_search import g_search

hellos = [u'你好', u'hello', u'hi']
s_hellos = ['你好', 'hello', 'hi']
e_happys = [':)', '^_^', 'O(∩_∩)O', '(◕‿‿◕)']


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
            sayhello = random.choice(s_hellos)
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
    q = '%s+%s'.encode('utf-8') % (songname, artist)
    image_url = ''.join([
        'http://api.douban.com/music/subjects?q=',
        q,
        '&alt=json&start-index=1&max-results=1',
    ])
    http_client = httpclient.HTTPClient()
    response = None
    music_image = None
    try:
        response = http_client.fetch(image_url)
    except httpclient.HTTPError as e:
        print("Error:", e)
    if response and response.code == 200:
        res = jload(response.body)
        music_image = res['entry'][0]['link'][2]['@href']
        music_image = '<img src="%s" style="float:left"/>' % music_image
        if not artist:
            artist = res['entry'][0]['author'][0]['name']['$t']

    singer = ''
    if artist:
        singer = '&singer=' + urllib.quote(artist.encode('gbk'))

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
    link = '<br/>'
    return music_image, link, songbox


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


def is_en(i):
    c = i.encode('utf-8')
    return True if len(c) == len(i) else False


def wiki(usersay):
    wiki = ''
    wikihints = [u'what is', u'who are', u'什么是', u'是什么', u'是谁', u'谁是']
    for i in wikihints:
        if i in usersay:
            usersay = usersay.replace(i, '')
            usersay = usersay.replace('?', '')
            usersay = usersay.encode("utf-8")
            wiki = g_search(usersay)
            break
    return wiki


def search_memo(usersay, userip):
    memo = ''
    lasthints = [u'上一句', u'前一句']
    for i in lasthints:
        if i in usersay:
            usersay = usersay.replace(i, '')
            usersay = usersay.replace('?', '')
            # memo = get_last(usersay) ['usersay']
            memo = Ande.find(
                {'user_ip': userip}).sort('_id', DESCENDING).limit(1)

            memo = u'你说的是:%s' % memo[0]['usersay']
            break
    return memo
