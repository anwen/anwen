
if __name__ == '__main__':
    import requests
    print('hi')
    usersay = raw_input()
    r = requests.get('http://localhost:8888/ande?q=1&usersay=%s' % usersay)
    print(r.text)

    # while True:
    #     usersay = raw_input()
    #     r = requests.get(
    #     	'http://localhost:8888/ande?q=1&usersay=%s' % usersay)
    #     print(r.text)
