from decimal import Decimal
from typing import Optional

from control.dto import TelegramResponseDto
from control.models import Match, User
from control.services import telegram_service, user_bet_service, user_service
from control.services.match_service import match_service


class TelegramRequestService:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls)

        return cls.instance

    def analyze_telegram_message(self, tg_dto: TelegramResponseDto) -> None:
        user = user_service.get_or_create_user_by_chat_id(tg_dto.chat_id)
        match = match_service.get_current_match()
        message = tg_dto.message
        chat_id = tg_dto.chat_id

        if message.startswith('begin'):
            message = message.replace('begin ', '')
            self.begin_match(user, chat_id, message, match)
        elif message.startswith('finish'):
            self.finish_match(message, chat_id, match)
        elif message.startswith('bet'):
            self.make_bet(message, chat_id, match)
        elif message.startswith('status'):
            self.check_status(user, match, chat_id)
        else:
            telegram_service.send_tg_message(chat_id, 'Unknown message type')

    def begin_match(self, user: User, chat_id: int, message: str, match: Optional[Match] = None) -> None:
        match_service.create_match(user, message, chat_id, match)
        telegram_service.send_tg_message(chat_id, 'ok')

    def finish_match(self, message, chat_id, match: Match) -> None:
        winner_team = match_service.hold_match_and_get_winner(match, chat_id, message)

        winners_list = []
        users = User.objects.filter_clients()
        for user in users:
            user_win_amount = user_bet_service.calculate_user_win(user, match, winner_team)
            if not user_win_amount:
                continue

            user.increment_balance(user_win_amount)
            winners_list.append(user)

        User.objects.bulk_update(users, ['balance'])
        telegram_service.notify_winners(winners_list)

    def make_bet(self, message: str, chat_id: int, match: Match) -> None:
        _, amount, side = message.split(' ')
        amount = Decimal(amount)
        user = User.objects.lock_user_by_chat_id(chat_id)
        bet_team = match_service.get_team_from_match(match, side, chat_id)
        user_bet_service.make_bet(user, match, bet_team, chat_id, amount)

        telegram_service.send_tg_message(chat_id, 'bet done. your balance now is {}'.format(user.balance))

    def check_status(self, user: User, match: Match, chat_id: int) -> None:
        if user.is_admin():
            telegram_service.send_tg_message(chat_id, 'error, only client can check status')
            return
        if match:
            telegram_service.send_tg_message(
                chat_id,
                f'current match “{match.team_a.name} vs {match.team_b.name}”, your balance is {user.balance}'
            )
        elif not match:
            telegram_service.send_tg_message(chat_id, f'There are not current mathces, your balance is {user.balance}')


telegram_request_service = TelegramRequestService()
