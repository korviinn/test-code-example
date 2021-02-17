from typing import Optional

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.response import Response

from control.services.tlg_service import TelegramService


class ClientRequest:
    client: Client

    def post(self, data: dict, reverse_path: str, path_params: Optional[dict] = None, **kwargs) -> Response:
        path = self.get_path(reverse_path, path_params, **kwargs)
        return self.client.post(path, data, content_type='application/json', **kwargs)

    def get_path(self, reverse_path: str, path_params: Optional[dict], **kwargs) -> str:
        if reverse_path:
            return reverse(reverse_path, kwargs=path_params)
        return kwargs.get('url')


class BaseTestCase(TestCase, ClientRequest):
    tlg = TelegramService()
    TEAM_A_NAME = 'TEAM A'
    TEAM_B_NAME = 'TEAM B'


class BaseProvider(ClientRequest):
    client = Client()
