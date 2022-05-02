from typing import Tuple

from .base import ACCESS_TOKEN_URL, wechat_request


class WechatAccessTokenUtils:
    @classmethod
    def get_one(cls) -> str:
        from car.models import WechatAccessToken

        token: WechatAccessToken = WechatAccessToken.objects.last()
        # NOTE: 这里只做兜底，我们会有定时任务刷新 token
        # TODO: 写一个定时任务刷新 token
        need_refresh = not token or token.last_expore_seconds < 60
        if need_refresh:
            new_token = cls.refresh_access_token()
            return new_token
        else:
            return token.access_token

    @classmethod
    def refresh_access_token(cls) -> str:
        from car.models import WechatAccessToken

        new_token, expires_in = cls._get_from_online()
        WechatAccessToken.objects.create(
            access_token=new_token,
            expires_in=expires_in,
        )
        return new_token

    @classmethod
    def _get_from_online(cls) -> Tuple[str, int]:
        url = ACCESS_TOKEN_URL
        res_json = wechat_request(url=url, method="GET")
        return res_json["access_token"], res_json["expires_in"]
