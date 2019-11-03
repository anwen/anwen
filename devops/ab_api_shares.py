import requests


url = 'https://anwensf.com/api/v2/shares?page=1'
url = 'https://anwensf.com/share/58247'

for i in range(10000000):
    print(i)
    res = requests.get(url)
    if res.status_code != 200:
        raise
