from decimal import Decimal
from typing import List, Union

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import ugettext_lazy as _


UserQs = Union[List['User'], QuerySet]


class UserManager(UserManager):
    def lock_user_by_chat_id(self, chat_id: int) -> 'User':
        return User.objects.select_for_update().get(chat_id=chat_id)

    def filter_clients(self) -> UserQs:
        return self.exclude(is_superuser=True).exclude(pk__in=settings.ADMIN_USERS_PK)


class User(AbstractUser):
    objects = UserManager()

    chat_id = models.CharField(max_length=255, unique=True)
    balance = models.DecimalField(default=1000.00, max_digits=8, decimal_places=2)
    email = models.EmailField(_('email address'), blank=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def is_admin(self):
        return self.pk in settings.ADMIN_USERS_PK or self.is_superuser

    def increment_balance(self, amount: Decimal) -> None:
        self.balance += amount

    def decrement_balance(self, amount: Decimal) -> None:
        self.balance = self.balance - amount
