import requests
from aiogram import types

from config import MAIN_HOST


async def get_user(message: types.Message):
    info_user = requests.get(f'{MAIN_HOST}/api/v1/fribit/users/{message.from_user.id}')
    data_user = info_user.json()
    return data_user


async def update_verifyer_code(message: types.Message, code):
    payload = {
        'code_verifier': code
    }
    responce = requests.patch(f'{MAIN_HOST}/api/v1/fribit/users/{message.from_user.id}/', data=payload)
    return responce.ok


async def set_access_token(data, telegram_user_id):
    payload = {'access_token': data['access_token'], 'refresh_token': data['refresh_token'],
               'user_id': data['user_id'], 'telegram_user_id': telegram_user_id}
    responce = requests.post(f'{MAIN_HOST}/api/v1/fribit/users/{telegram_user_id}/', data=payload)
    return responce.ok


async def get_user_rating(telegram_user_id):
    responce = requests.get(f'{MAIN_HOST}/rating/{telegram_user_id}/')
    return responce.json()
