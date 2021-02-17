from core.errors import TelegramApiError


class UserIsNotAdminError(TelegramApiError):
    exc_type = 'user_is_not_admin'
    msg = 'User is not admin'


class UserIsAminError(TelegramApiError):
    exc_type = 'user_is_admin'
    msg = 'User is admin!'


class MatchAlreadyExists(TelegramApiError):
    exc_type = 'match_exists'
    msg = 'Match already exists'


class MatchDoesNotExists(TelegramApiError):
    exc_type = 'match_does_not_exists'
    msg = 'Match does not exists'


class TeamNotFound(TelegramApiError):
    exc_type = 'team_not_found'
    msg = 'Team not found'


class NotEnoughMoney(TelegramApiError):
    exc_type = 'not_enough_money'
    msg = 'Not enough money'
