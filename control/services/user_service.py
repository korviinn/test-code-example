from decimal import Decimal

from control.models import User


class UserService:
    def get_or_create_user_by_chat_id(self, chat_id: int) -> User:
        try:
            return User.objects.get(chat_id=chat_id)
        except User.DoesNotExist:
            # some random data that doesn't matter for current project
            return User.objects.create(
                chat_id=chat_id,
                username=chat_id,
                email='{}@mail.ru'.format(chat_id)
            )

    def withdraw_balance(self, user: User, amount: Decimal) -> None:
        user.decrement_balance(amount)
        user.save()


user_service = UserService()
