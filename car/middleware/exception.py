import logging
from typing import List

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
        return http_response(
            request=request,
            data={"errors": errors},
            status_code=400,
        )
