import requests
import random, string
import datetime
from time import sleep

V2B_REG_REL_URL = '/api/v1/passport/auth/register'
# V2B_SUB_REL_URL = '/api/v1/user/getSubscribe'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'

home_url = 'https://sub.chbjpw.mobi'
times = 10000
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

headers = {'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '',
    'DNT': '1',
    'Host': home_url[home_url.find('//')+2:],
    'Origin': home_url,
    'Referer': home_url,
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers',
    'User-Agent': USER_AGENT}

subs = []
i = 0
while i < times:
    form_data = {'email': ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(12))+'@gmail.com',
                'password': 'autosub_v2b',
                'invite_code': '',
            'email_code': ''}
    try:
        response = requests.post(home_url+V2B_REG_REL_URL, json=form_data, proxies=proxies)
    except:
        continue
    # print(response.text)
    try:
        subscription_url = f'{home_url}/api/v1/client/subscribe?token={response.json()["data"]["token"]}'
        subs.append(subscription_url)
    except:
        print(f'Invalid response: {response.text.encode("utf-8")}')
        sleep(3)
    else:
        i += 1
        print(f'Number succeeded: {i}\t{subscription_url}')

print(f'{times} accounts created. Subscription URLs:\n----------')
print(*subs, sep='\n')
