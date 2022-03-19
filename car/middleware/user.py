"""
sessionid = user.id 加密后的字符串
"""


from typing import Dict, Set

from django.urls import resolve

from car.models import User


class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        from car.service.user import NULL_USER, UserService

        user: User
        url_name = resolve(request.path_info).url_name
        if self.no_need_sessionid(url_name, request.method):
            user = NULL_USER
        else:
            sessionid = request.COOKIES.get("sessionid") or ""
            user_id = UserService.get_user_id(sessionid)
            if user_id is None:
                from car.utils.http import http_response

                return http_response(request=request, message="尚未登录", status_code=403)
            user = UserService.get_one(user_id)
        setattr(request, "user", user)
        response = self.get_response(request)
        return response

    @classmethod
    def no_need_sessionid(cls, url_name: str, method: str) -> bool:
        url_name_methds_white_list: Dict[str, Set[str]] = {
            "goods": {"GET"},
            "wechat_login": {"POST"},
            "wechat_callback": {"GET"},
        }
        return method.upper() in url_name_methds_white_list.get(url_name, set())
