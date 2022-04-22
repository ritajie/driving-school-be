import logging
import traceback

from django.http import HttpRequest, HttpResponse

from car.utils.http import http_response

logger = logging.getLogger(__name__)


def handler500(request: HttpRequest) -> HttpResponse:
    error = "Internal Server Error"
    logger.error(traceback.format_exc())
    return http_response(
        request=request,
        message=error,
        status_code=400,
    )
