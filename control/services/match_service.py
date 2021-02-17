from enum import Enum

from control.errors import MatchAlreadyExists, MatchDoesNotExists, TeamNotFound, UserIsNotAdminError
from control.models import Match, Team, User


class SideEnum(Enum):
    left = 'left'
    right = 'right'


class MatchService:
    def get_current_match(self) -> Match:
        return Match.objects.filter(is_active=True).first()

    def create_match(self, user: User, message: str, chat_id: int, match: Match) -> None:
        if not user.is_admin():
            raise UserIsNotAdminError(chat_id)
        if match:
            raise MatchAlreadyExists(chat_id)
        a, b = message.split(' vs ')
        team_a, _ = Team.objects.get_or_create(name=a)
        team_b, _ = Team.objects.get_or_create(name=b)

        Match.objects.create(team_a=team_a, team_b=team_b)

    def hold_match_and_get_winner(self, match: Match, chat_id: int, message: str) -> Team:
        if not match:
            raise MatchDoesNotExists(chat_id)

        won_team = message.split(' ')[1]
        winner = self.get_team_from_match(match, won_team, chat_id)

        match.disable(winner)
        return winner

    def get_team_from_match(self, match: Match, side: str, chat_id: int) -> Team:
        if side == SideEnum.left.value:
            team = match.team_a
        elif side == SideEnum.right.value:
            team = match.team_b
        else:
            # ._send_tg_message(chat_id, 'error. Use "left" or "right" word to select team')
            raise TeamNotFound(chat_id)

        return team

    def validate_user_role(self, user: User):
        if not user.is_admin():
            raise UserIsNotAdminError()


match_service = MatchService()
