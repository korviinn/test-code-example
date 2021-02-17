# from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin

from control.views import TelegramApiView


admin.autodiscover()


urlpatterns = [
    url(
        r'^telegram/{webhook}/'.format(webhook=settings.TELEGRAM_WEBHOOK),
        TelegramApiView.as_view(), name='telegram'
    ),
    url(r'^admin/', admin.site.urls),
]
