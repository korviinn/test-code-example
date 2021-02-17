from control.tests.base_test import BaseProvider
from control.tests.consts import TELEGRAM_REVERSE_URL


class MatchProvider(BaseProvider):
    def create_match(self, chat_id: int, team_a: str, team_b: str) -> int:
        data = {
            'update_id': 1,
            'message': {
                'chat': {'id': chat_id},
                'message_id': 1,
                'text': f'begin {team_a} vs {team_b}'
            }
        }
        self.post(data, TELEGRAM_REVERSE_URL)
        return chat_id

    def make_bet(self, chat_id: int, amount: int, side: str):
        data = {
            'update_id': 1,
            'message': {
                'chat': {'id': f'{chat_id}'},
                'message_id': 1,
                'text': f'bet {amount} {side}'
            }
        }
        self.post(data, TELEGRAM_REVERSE_URL)
        return chat_id


match_provider = MatchProvider()
