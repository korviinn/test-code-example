import logging

from django.db.transaction import atomic
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from control.services.telegram_request_service import telegram_request_service
from .serializers import TelegramJsonDataSerializer


logger = logging.getLogger(__name__)


class TelegramApiView(APIView):
    permission_classes = [AllowAny]

    @atomic()
    def post(self, request, *args, **kwargs) -> Response:
        serializer = TelegramJsonDataSerializer(data=request.data)

        if not serializer.is_valid():
            logger.error(serializer.errors)
            return Response({})

        try:
            tg_dto = serializer.get_telegram_dto()
            telegram_request_service.analyze_telegram_message(tg_dto)
        except Exception as e:
            # we shouldn't raise any exceptions in telegram webhook view
            # other way telegram will send us message non-stoppable untile of 200 http response
            logger.error(e)

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
