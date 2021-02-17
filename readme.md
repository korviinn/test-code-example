This is code example
That is test project about betting system.
There are 2 roles - admin and clients.

All communication with this app going through telegram bot.

Admin - can create matches with two teams.
Clients - can make bet on any team of active match and can check their balance and bet status.
In the end Admin close match. Choose win team. 
Users that win - get balance fillup and notification about winning.

To run test use:
python manage.py test --settings='core.settings.test'

To run project:
- your need to set telegram token
- set django secret key
