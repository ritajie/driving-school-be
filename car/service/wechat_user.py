from urllib.parse import urljoin

import requests
from django.conf import settings

from car.models import WechatUser

WECHAT_API = "https://api.weixin.qq.com"
WECHAT_ACCESS_TOKEN_PATH = f"/sns/oauth2/access_token?appid={settings.WECHAT_APP_ID}&secret={settings.WECHAT_APP_SECRET}&code={'{}'}&grant_type=authorization_code"
WECHAT_USER_INFO_PATH = "/sns/userinfo?access_token={}&openid=OPENID&lang=zh_CN"


class WechatUserService:
    @classmethod
    def get_one(cls, code: str) -> WechatUser:
        access_token = cls._get_access_token(code)
        user_info = cls._get_user_info(access_token)
        return WechatUser(
            openid=user_info["openid"],
            nickname=user_info["nickname"],
            sex=user_info["sex"],
            language=user_info["language"],
            city=user_info["city"],
            province=user_info["province"],
            country=user_info["country"],
            headimgurl=user_info["headimgurl"],
            privilege=user_info["privilege"],
        )

    @classmethod
    def _get_access_token(cls, code: str) -> str:
        url = urljoin(WECHAT_API, WECHAT_ACCESS_TOKEN_PATH.format(code))
        res = requests.get(url)
        return res.json()["access_token"]

    @classmethod
    def _get_user_info(cls, access_token: str) -> dict:
        url = urljoin(WECHAT_API, WECHAT_USER_INFO_PATH.format(access_token))
        res = requests.get(url)
        res.encoding = "utf-8"
        return res.json()
