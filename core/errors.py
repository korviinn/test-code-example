from typing import Optional

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import exception_handler as drf_exception_handler


class MainExceptionHandler:
    reserved_error_names = ['type', 'message', 'errors']

    def __call__(self, exc, context):
        return self.handle_exceptions(exc, context)

    def handle_exceptions(self, exc, context):
        response = drf_exception_handler(exc, context)
        return self.format_errors_response(response)

    def format_errors_response(self, response: Response) -> Response:
        if response is not None:
            if not response.data.get('type'):
                response.data['type'] = None
        return response


main_exception_handler = MainExceptionHandler()


class TelegramApiError(APIException):
    '''
    make note that current exception returns HTTP_200 Response
    use it only in telegram exception handlers
    '''

    msg: str
    exc_type: str
    status_code = HTTP_200_OK

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        instance.default_detail = {
            'message': cls.msg,
            'type': cls.exc_type,
        }
        return instance

    def __init__(self, chat_id: Optional[int] = None, *args, **kwargs):
        self.log_msg = f'{self.msg}, {chat_id}'
        super().__init__(*args, **kwargs)
