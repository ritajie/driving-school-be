import json
from datetime import datetime

from django.http import HttpRequest, HttpResponse


def http_response(
    request: HttpRequest,
    message="",
    data={},
    status_code=200,
) -> HttpResponse:
    def datetime_to_timestamp(obj: datetime):
        if isinstance(obj, datetime):
            return int(datetime.timestamp(obj))
        return obj

    body_content = {"code": status_code, "message": message, "data": data}
    # 序列化json as body
    body_content_str = json.dumps(body_content, default=datetime_to_timestamp)
    response = HttpResponse(body_content_str, "application/json")
    return response
