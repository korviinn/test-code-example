from control.tests.providers.user_provider import user_provider
from .base_test import BaseTestCase
from .consts import TELEGRAM_REVERSE_URL
from .providers.match_provider import match_provider
from ..models import Match, Team, User, UserBet


class TelegramServiceTestCase(BaseTestCase):
    def setUp(self):
        admin_chat_id = user_provider.create_user()
        self.admin = User.objects.get(chat_id=admin_chat_id)
        self.admin.is_superuser = True
        self.admin.save()

        client_chat_id = user_provider.create_user()
        self.customer = User.objects.get(chat_id=client_chat_id)

    def test_create_match(self):
        data = {
            'update_id': 1,
            'message': {
                'chat': {'id': f'{self.admin.chat_id}'},
                'message_id': 1,
                'text': f'begin {self.TEAM_A_NAME} vs {self.TEAM_B_NAME}'
            }
        }
        self.post(data, TELEGRAM_REVERSE_URL)
        self.assertEqual(Match.objects.filter(is_active=True).count(), 1)
        self.assertEqual(Team.objects.all().count(), 2)

    def test_make_bet(self):
        match_provider.create_match(self.admin.chat_id, 'team_a', 'team_b')
        data = {
            'update_id': 1,
            'message': {
                'chat': {'id': f'{self.customer.chat_id}'},
                'message_id': 1,
                'text': 'bet 100 left'
            }
        }
        self.post(data, TELEGRAM_REVERSE_URL)

        customer = User.objects.get(id=self.customer.id)
        self.assertEqual(customer.balance, 900.00)
        self.assertEqual(UserBet.objects.filter(user=customer).count(), 1)

    def test_customer_status(self):
        # that case should be covered by unittest
        match_provider.create_match(self.admin.chat_id, 'team_a', 'team_b')
        match_provider.make_bet(self.customer.chat_id, 100, 'left')
        data = {
            'update_id': 1,
            'message': {
                'chat': {'id': f'{self.customer.chat_id}'},
                'message_id': 1,
                'text': 'status'
            }
        }
        self.post(data, TELEGRAM_REVERSE_URL)

    def test_finish_match_with_customer_win(self):
        winner = 'team_a'
        match_provider.create_match(self.admin.chat_id, winner, 'team_b')
        match_provider.make_bet(self.customer.chat_id, 100, 'left')
        data = {
            'update_id': 1,
            'message': {
                'chat': {'id': f'{self.customer.chat_id}'},
                'message_id': 1,
                'text': 'finish left'
            }
        }
        self.post(data, TELEGRAM_REVERSE_URL)

        customer = User.objects.get(id=self.customer.id)
        self.assertEqual(customer.balance, 1100.00)
        self.assertEqual(Match.objects.all()[0].winner, Team.objects.get(name=winner))

    def test_finish_match_with_customer_loose(self):
        winner = 'team_b'
        match_provider.create_match(self.admin.chat_id, 'team_a', winner)
        match_provider.make_bet(self.customer.chat_id, 100, 'left')
        data = {
            'update_id': 1,
            'message': {
                'chat': {'id': f'{self.customer.chat_id}'},
                'message_id': 1,
                'text': 'finish right'
            }
        }
        self.post(data, TELEGRAM_REVERSE_URL)

        customer = User.objects.get(id=self.customer.id)
        self.assertEqual(customer.balance, 900.00)
        self.assertEqual(Match.objects.all()[0].winner, Team.objects.get(name=winner))
