import ssl
from typing import Optional

import aiohttp
from aiohttp import BasicAuth


async def get(url):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context),
            trust_env=True
    ) as session:
        async with session.get(url) as response:
            return await response.json()


async def post(url, data):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context),
            trust_env=True
    ) as session:
        async with session.post(url, data=data) as response:
            return await response.text()


async def get_image_from_bo(url, data):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context),
            trust_env=True
    ) as session:
        async with session.post(url, data=data) as response:
            return await response.read()


async def get_image(url):
    """Получает изображение из Telegram по указанному URL.

    Асинхронно устанавливает безопасное соединение с помощью
    aiohttp.ClientSession.

    Args:
        url (str): URL для получения изображения.

    Returns:
        bytes: Двоичные данные изображения.
    """
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context),
            trust_env=True
    ) as session:
        async with session.get(url) as response:
            return await response.read()


async def post_jira_bp(
        url: str,
        data,
        username: Optional[str] = None,
        password: Optional[str] = None
):
    """Асинхронно отправляет данные на конечную точку JIRA.

    Args:
        url (str): URL конечной точки JIRA.
        data: Данные для отправки.
        username (str, optional): Имя пользователя для аутентификации.
        По умолчанию None.
        password (str, optional): Пароль для аутентификации. По умолчанию None.

    Returns:
        aiohttp.ClientResponse: Объект ответа от POST-запроса.
    """
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    headers = {"Content-Type": "application/json"}

    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context),
            trust_env=True
    ) as session:
        auth = BasicAuth(username, password) if username and password else None
        async with session.post(
                url,
                data=data,
                headers=headers,
                auth=auth
        ) as response:
            return response
