from auraframes.client import Client


class BaseApi:
    def __init__(self, client: Client):
        self._client = client
