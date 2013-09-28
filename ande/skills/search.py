def search(a):
    if a.startswith('!g '):
        a = a.replace('!g ', '')
        return search_g(a, 'web')
    return ''


def search_g(a, r_type):
    # http://ajax.googleapis.com/ajax/services/search/web
    # ?v=5.0&start=10&rsz=2&q=hi
    url = ''.join([
        'http://ajax.googleapis.com/ajax/services/search/'
        '%s' % r_type,
        '?v=1.0',
        '&start=10&rsz=5&q=%s' % a,
    ])
    import requests
    r = requests.get(url)
    return r.text
