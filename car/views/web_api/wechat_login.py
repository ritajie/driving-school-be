import json

from django.views.generic import View

from car.models import UserType
from car.service.user import UserService
from car.service.wechat_user import WechatUserService
from car.utils.http import http_response


class WechatLoginView(View):
    def post(self, request):
        body = json.loads(request.body)
        code = body["code"]

        wechat_user = WechatUserService.get_one(code=code)
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

        return http_response(
            request=request,
            data={
                "sessionid": UserService.gen_sessionid(user.id),
            },
        )
