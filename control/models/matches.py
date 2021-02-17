from typing import List, Union

from django.db.models import BooleanField, CASCADE, CharField, DecimalField, ForeignKey, Manager, Model, QuerySet, Sum

from control.types import UserId


TeamQs = Union[List['Team'], QuerySet]
MatchQs = Union[List['Match'], QuerySet]
UserBetQs = Union[List['UserBet'], QuerySet]


class Team(Model):
    name = CharField(max_length=255)


class Match(Model):
    team_a = ForeignKey(Team, related_name='a_team', on_delete=CASCADE)
    team_b = ForeignKey(Team, related_name='b_team', on_delete=CASCADE)
    winner = ForeignKey(Team, related_name='winner_team', null=True, on_delete=CASCADE)
    is_active = BooleanField(default=True)

    def disable(self, winner):
        self.is_active = False
        self.winner = winner
        self.save()


class UserBetManager(Manager):
    def filter_winner_bets(self, user_id: UserId, match: Match, winner: Team) -> UserBetQs:
        return self.filter(match=match, team=winner, user_id=user_id)

    def calculate_win_sum(self, user_id: UserId, match: Match, winner: Team) -> UserBetQs:
        qs = self.filter_winner_bets(user_id, match, winner)
        return qs.aggregate(Sum('ammount'))


class UserBet(Model):
    objects = UserBetManager()

    user = ForeignKey('control.User', on_delete=CASCADE)
    match = ForeignKey(Match, on_delete=CASCADE)
    team = ForeignKey(Team, on_delete=CASCADE)
    ammount = DecimalField(max_digits=8, decimal_places=2)
