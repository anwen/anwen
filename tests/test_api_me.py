import requests
import json
from pathlib import Path
import os
import random
api_base = 'https://anwensf.com/'
api_base = 'http://localhost:8888/'


def format_json(ajson):
    ajson = json.dumps(ajson, indent=4, ensure_ascii=False)
    print(ajson)
    return ajson


def test_auth_by_password():
    api = api_base + 'api/authorizations'
    email = 'askender43@gmail.com'
    print('please input your password of {}:'.format(email))
    password = input()
    params = {}
    params['email'] = email
    params['password'] = password
    r = requests.get(api, params=params)
    r = r.json()
    format_json(r)
    token = r['data']['token']
    home = str(Path.home())
    print(home)
    f_token = os.path.join(home, '.anwen_token')
    with open(f_token, 'w') as f:
        f.write(token+'\n')
    print(token)


def test_me():
    # 取出token
    home = str(Path.home())
    f_token = os.path.join(home, '.anwen_token')
    token = open(f_token).read().strip()
    print(token)

    api = api_base + 'api/me'
    headers = {}
    headers['Authorization'] = 'token {}'.format(token)

    r = requests.get(api, headers=headers)
    format_json(r.json())

    ajson = {}
    ajson['say'] = random.choice(['just for fun!', 'just for fun'])
    # r = requests.post(api, headers=headers, params=ajson) # both ok
    r = requests.post(api, headers=headers, json=ajson)
    format_json(r.json())

    r = requests.get(api, headers=headers)
    format_json(r.json())

    ajson = {}
    ajson['tags'] = '读书,写字'
    r = requests.post(api, headers=headers, json=ajson)
    format_json(r.json())

    ajson = {}
    ajson['remove_tag'] = '写字'
    r = requests.post(api, headers=headers, json=ajson)
    format_json(r.json())


if __name__ == '__main__':
    # test_auth_by_password()
    test_me()
