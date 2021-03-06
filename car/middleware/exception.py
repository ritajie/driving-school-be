import logging
from typing import List

from car.models import ServiceError
from car.utils.http import http_response


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logging.exception(exception)
        errors: List[str] = [type(exception).__name__, str(exception)]

        if isinstance(exception, ServiceError):
            message = str(exception)
        else:
            message = "服务器错误"
        return http_response(
            request=request,
            data={"errors": errors},
            message=message,
            status_code=400,
        )
