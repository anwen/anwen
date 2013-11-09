import sys
import requests

if __name__ == '__main__':
    usersay = sys.argv[1]
    r = requests.get(
        'http://localhost:8888/ande?q=1&usersay=%s' % usersay)
    print('Ande say:%s' % r.text)
    sys.exit(0)
    while True:
        usersay = raw_input('You say:')
        r = requests.get(
            'http://localhost:8888/ande?q=1&usersay=%s' % usersay)
        print('Ande say:%s' % r.text)
