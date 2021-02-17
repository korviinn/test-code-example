from django.conf import settings
from telebot import TeleBot

from control.models.users import UserQs
from control.tests.helpers import skip_in_tests


class TelegramService:
    def __init__(self):
        self.tb = TeleBot(settings.TELEGRAM_TOKEN)

    def notify_winners(self, users: UserQs) -> None:
        for user in users:
            client_msg = f'you win. your balance now is {user.balance}'
            telegram_service.send_tg_message(user.chat_id, client_msg)

    @skip_in_tests
    def send_tg_message(self, chat_id: int, message: str) -> None:
        '''
        Send Message to Telegram
        '''
        self.tb.send_message(chat_id, message)


telegram_service = TelegramService()
