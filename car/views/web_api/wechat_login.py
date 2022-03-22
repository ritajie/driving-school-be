import json
from typing import Union

from django.views.generic import View

from car.models import Coach, User, UserType, WechatUser
from car.service.coach import CoachService
from car.service.session import SessionIDService
from car.service.user import UserService
from car.service.wechat_user import WechatUserService
from car.utils.http import http_response


class WechatLoginView(View):
    def post(self, request):
        body = json.loads(request.body)
        code = body["code"]
        is_coach = body.get("is_coach", False)
        wechat_user = WechatUserService.get_one(code=code)

        user_or_coach: Union[User, Coach]
        if is_coach:
            user_or_coach = self._get_or_create_coach(wechat_user)
        else:
            user_or_coach = self._get_or_create_user(wechat_user)

        return http_response(
            request=request,
            data={
                "sessionid": SessionIDService.gen_sessionid(user_or_coach),
            },
        )

    @classmethod
    def _get_or_create_user(cls, wechat_user: WechatUser) -> User:
        users = UserService.get_list(
            types=[UserType.Wechat],
            platform_openids=[wechat_user.openid],
        )
        is_new_user = not users
        if is_new_user:
            user = UserService.create(
                name=wechat_user.nickname,
                phone="",
                platform_openid=wechat_user.openid,
                type=UserType.Wechat,
                headimg=wechat_user.headimgurl,
            )
        else:
            user = users[0]
        return user

    @classmethod
    def _get_or_create_coach(cls, wechat_user: WechatUser) -> Coach:
        coaches = CoachService.get_list(
            types=[UserType.Wechat],
            platform_openids=[wechat_user.openid],
        )
        is_new_coach = not coaches
        if is_new_coach:
            coach = CoachService.create(
                name=wechat_user.nickname,
                phone="",
                platform_openid=wechat_user.openid,
                type=UserType.Wechat,
                headimg=wechat_user.headimgurl,
            )
        else:
            coach = coaches[0]
        return coach
