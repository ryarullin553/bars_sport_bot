import base64
import datetime
import hashlib
import os

import requests
from authlib.common.security import generate_token

from config import (
    FITBIT_AUTHORIZATION_TOKEN_ENDPOINT,
    FITBIT_AUTHORIZATION_ENDPOINT,
    FITBIT_CLIENT_ID,
    FITBIT_CLIENT_SECRET
)


async def get_auth_link():
    client_id = FITBIT_CLIENT_ID
    auth_url = FITBIT_AUTHORIZATION_ENDPOINT

    scope = 'activity'

    code_verifier = generate_token(128)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8')[:-1]

    url = f'{auth_url}?response_type=code&client_id={client_id}&scope={scope}&code_challenge={challenge}&code_challenge_method=S256&state=0b5o2b100z1o5k0v4x440x0q0s5x694r'

    return url, code_verifier


async def auth(code, verifier):
    client_id = FITBIT_CLIENT_ID
    client_secret = FITBIT_CLIENT_SECRET

    auth = base64.b64encode(f'{client_id}:{client_secret}'.encode("utf-8")).decode("utf-8")

    url = "https://api.fitbit.com/oauth2/token"

    payload = f'grant_type=authorization_code&code={code}&client_id={client_id}&code_verifier={verifier}'
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6,ja;q=0.5',
        'authorization': f'Basic {auth}',
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        return None
    else:
        return response.json()

async def get_today_activity(token, user_id):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    today = datetime.date.today()

    url = f'https://api.fitbit.com/1/user/{user_id}/activities/date/{today.isoformat()}.json'

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    else:
        return response.json()