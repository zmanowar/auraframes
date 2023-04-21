from collections import deque
from typing import Optional, Deque

import httpx
from httpx import Response, Timeout
from loguru import logger

AURA_API_BASE_URL = 'https://api.pushd.com'
AURA_API_VERSION = 'v5'
USER_AGENT = 'Aura/4.7.790 (Android 30; Client)'


# Use something similar to:
# https://github.com/sudoguy/tiktokpy/blob/master/tiktokpy/client/__init__.py
# https://github.com/mkb79/Audible/tree/master/src/audible
# https://github.com/ssut/py-googletrans/blob/master/googletrans/client.py


# TODO: This should be reworked to be async, particularly for mass uploads/clones.

class Client:

    def __init__(self, history_len: int = 30):
        self.http2_client = httpx.Client(http2=True, base_url=f'{AURA_API_BASE_URL}/{AURA_API_VERSION}', headers={
            'accept-language': 'en-US',
            'cache-control': 'no-cache',
            'user-agent': USER_AGENT,
            'content-type': 'application/json; charset=utf-8',
        }, timeout=Timeout(timeout=20.0))

        self.history: Deque[Response] = deque(maxlen=history_len)

    def get(self, url, query_params: Optional[dict] = None, headers: Optional[dict] = None):
        query_params = {k: v for k, v in query_params.items() if v is not None} if query_params else None
        logger.info(f'GET request to {url}', query_params=query_params, headers=headers)
        response = self.http2_client.get(url=url, params=query_params, headers=headers)

        self.history.append(response)
        logger.debug(f'Response ({response.status_code}), body: {response.json()}')

        self._set_cookies(response)

        return response.json()

    def post(self, url, data: dict = None, query_params: Optional[dict] = None, headers: Optional[dict] = None):
        logger.info(f'POST request to {url}', data=data, query_params=query_params, headers=headers)
        response = self.http2_client.post(url=url, json=data, headers=headers, params=query_params)

        self.history.append(response)
        logger.debug(f'Response ({response.status_code}), body: {response.json()}')

        self._set_cookies(response)

        return response.json()

    def delete(self, url, query_params: Optional[dict] = None, headers: Optional[dict] = None):
        logger.info(f'DELETE request to {url}', query_params=query_params, headers=headers)
        response = self.http2_client.delete(url=url, headers=headers, params=query_params)

        self.history.append(response)
        logger.debug(f'Response ({response.status_code}), body: {response.json()}')

        self._set_cookies(response)

        return response.json()

    def put(self, url, data: dict = None, query_params: Optional[dict] = None, headers: Optional[dict] = None):
        logger.info(f'PUT request to {url}', data=data, query_params=query_params, headers=headers)
        response = self.http2_client.put(url=url, json=data, headers=headers, params=query_params)

        self.history.append(response)
        logger.debug(f'Response ({response.status_code}), body: {response.json()}')

        self._set_cookies(response)

        return response.json()

    def add_default_headers(self, headers: dict) -> None:
        self.http2_client.headers.update(headers)

    def _set_cookies(self, response: httpx.Response) -> None:
        if len(response.cookies):
            logger.debug(f'Response Cookies: {response.cookies}')

        for cookie_name, cookie_data in response.cookies.items():
            self.http2_client.cookies.set(cookie_name, cookie_data)
