from rest_framework import serializers

from control.dto import TelegramResponseDto
from core.errors import TelegramApiError


class TelegramValidationErrorTelegram(TelegramApiError):
    msg = ''
    exc_type = 'validation error'


class TelegramMessageJsonDataSerializer(serializers.Serializer):
    chat = serializers.DictField(required=True)
    message_id = serializers.IntegerField(required=True)
    text = serializers.CharField(required=True)


class TelegramJsonDataSerializer(serializers.Serializer):
    update_id = serializers.IntegerField(required=True)
    message = TelegramMessageJsonDataSerializer(required=True)

    def get_telegram_dto(self) -> TelegramResponseDto:
        message = self.validated_data.get('message', {})
        chat = message.get('chat', {})
        chat_id = chat.get('id')
        if not chat_id:
            raise TelegramValidationErrorTelegram()

        return TelegramResponseDto(chat_id, message.get('text'))
