"""
Interface to Microsoft Translator API
I wrote one with php
This one is form https://github.com/bahn/bingtrans  Thanks
"""
import urllib
import codecs
import json

api_url = "http://api.microsofttranslator.com/V2/Ajax.svc/Translate"
#  Bing Developer Center申请ApiId。安德的测试可以用下面的appid 支持自动识别语言
app_id = '5853B784F9DAF5C32487D3C958510F127FF99011'


def _unicode_urlencode(params):
    """
    A unicode aware version of urllib.urlencode.
    Borrowed from pyfacebook :: http://github.com/sciyoshi/pyfacebook/
    """
    if isinstance(params, dict):
        p = params.items()
    i = [(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in p]
    return urllib.urlencode(i)


def _run_query(args):
    """
    takes arguments and optional language argument and runs query on server
    """
    data = _unicode_urlencode(args)
    sock = urllib.urlopen(api_url + '?' + data)
    result = sock.read()
    if result.startswith(codecs.BOM_UTF8):
        result = result.lstrip(codecs.BOM_UTF8).decode('utf-8')
    elif result.startswith(codecs.BOM_UTF16_LE):
        result = result.lstrip(codecs.BOM_UTF16_LE).decode('utf-16-le')
    elif result.startswith(codecs.BOM_UTF16_BE):
        result = result.lstrip(codecs.BOM_UTF16_BE).decode('utf-16-be')
    return json.loads(result)


def set_app_id(new_app_id):
    global app_id
    app_id = new_app_id


def translate(text, source='', target='zh-cn', html=False):
    """
    action=opensearch
    """
    if not app_id:
        raise ValueError("AppId needs to be set by set_app_id")
    query_args = {
        'appId': app_id,
        'text': text,
        'from': source,
        'to': target,
        'contentType': 'text/plain' if not html else 'text/html',
        'category': 'general'
    }
    return _run_query(query_args)

# set_app_id('5853B784F9DAF5C32487D3C958510F127FF99011')
# you can get your AppID at: http://www.bing.com/developers/

if __name__ == '__main__':
    print translate('hello', 'en', 'zh-cn')
    usersay = u'你好'.encode("utf-8")
    print translate(usersay, '', 'en')
