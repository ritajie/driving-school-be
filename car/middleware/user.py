"""
sessionid = user.id 加密后的字符串
"""


from typing import Dict, Optional, Set

from django.urls import resolve

from car.models import Coach, User


class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        from car.service.session import SessionIDService

        user: Optional[User] = None
        coach: Optional[Coach] = None
        url_name = resolve(request.path_info).url_name
        if self.no_need_login(url_name, request.method):
            user = None
        else:
            sessionid = request.COOKIES.get("sessionid") or ""
            if sessionid:
                user, coach = SessionIDService.parse_sessionid(sessionid)
            else:
                user = None
                coach = None
            if user is None and coach is None:
                from car.utils.http import http_response

                return http_response(request=request, message="尚未登录", status_code=403)
        setattr(request, "user", user)
        setattr(request, "coach", coach)
        response = self.get_response(request)
        return response

    @classmethod
    def no_need_login(cls, url_name: str, method: str) -> bool:
        url_name_methds_white_list: Dict[str, Set[str]] = {
            "goods": {"GET"},
            "wechat_login": {"POST"},
            "wechat_callback": {"GET"},
        }
        return method.upper() in url_name_methds_white_list.get(url_name, set())
