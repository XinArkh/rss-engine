"""
Identify verification code, using YunMa Server.

https://www.jfbym.com/
"""

import json
import base64
import requests

from user_api import yunma_token


def identify_verifycode(img_bin):
    img_b64_str = base64.b64encode(img_bin).decode()

    api_url = "https://www.jfbym.com/api/YmServer/customApi"
    headers = {'Content-Type': 'application/json'}
    payload = {'image': img_b64_str, 
           'token': yunma_token,
           'type': '10104'}
    r = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if not r.status_code == 200:
        raise Exception('YunMa Error: %s' % r.text)

    return r.json()['data']['data']
