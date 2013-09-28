
if __name__ == '__main__':
    import requests
    r = requests.get(
        'http://localhost:8888/ande?q=1')
    print('Ande say:%s' % r.text)
    while True:
        usersay = raw_input('You say:')
        r = requests.get(
            'http://localhost:8888/ande?q=1&usersay=%s' % usersay)
        print('Ande say:%s' % r.text)
