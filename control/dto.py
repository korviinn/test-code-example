class TelegramResponseDto:
    def __init__(self, chat_id: int, message: str):
        self.chat_id = chat_id
        self.message = message
