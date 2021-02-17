from random import randint

from control.tests.base_test import BaseProvider
from control.tests.consts import TELEGRAM_REVERSE_URL


class UserProvider(BaseProvider):
    def create_user(self) -> int:
        chat_id = randint(0, 100000)

        data = {
            'update_id': 1,
            'message': {
                'chat': {'id': chat_id},
                'message_id': 1,
                'text': 'status'
            }
        }
        self.post(data, TELEGRAM_REVERSE_URL)
        return chat_id


user_provider = UserProvider()
