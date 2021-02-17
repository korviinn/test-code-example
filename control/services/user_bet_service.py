from decimal import Decimal
from typing import Optional

from control.errors import MatchDoesNotExists, NotEnoughMoney, UserIsAminError
from control.models import Match, Team, User, UserBet
from control.services import user_service


class UserBetService:
    def calculate_user_win(self, user: User, match: Match, winner: Team) -> Optional[Decimal]:
        user_win_amount = UserBet.objects.calculate_win_sum(user.id, match, winner)['ammount__sum']

        if user_win_amount is None:
            return

        return Decimal(user_win_amount) * 2

    def make_bet(self, user: User, match: Match, bet_team: Team, chat_id: int, amount: Decimal) -> None:
        self.run_make_bet_validation(user, match, chat_id, amount)
        user_service.withdraw_balance(user, amount)
        UserBet.objects.create(ammount=amount, team=bet_team, match=match, user=user)

    def run_make_bet_validation(self, user: User, match: Match, chat_id: int, amount: Decimal) -> None:
        if user.is_admin():
            raise UserIsAminError(chat_id)
        if not match:
            raise MatchDoesNotExists(chat_id)
        if user.balance < amount:
            raise NotEnoughMoney(chat_id)
            # self._send_tg_message(chat_id, 'You have not got enough money')


user_bet_service = UserBetService()
