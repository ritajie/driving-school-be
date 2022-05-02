from .base import WECHAT_ACCESS_TOKEN_URL, WECHAT_USER_INFO_URL, wechat_request


class WechatUserUtils:
    @classmethod
    def get_one(cls, code: str) -> dict:
        access_token = cls._get_access_token(code)
        user_info = cls._get_user_info(access_token)
        return {
            "openid": user_info["openid"],
            "nickname": user_info["nickname"],
            "sex": user_info["sex"],
            "language": user_info["language"],
            "city": user_info["city"],
            "province": user_info["province"],
            "country": user_info["country"],
            "headimgurl": user_info["headimgurl"],
            "privilege": user_info["privilege"],
        }

    @classmethod
    def _get_access_token(cls, code: str) -> str:
        url = WECHAT_ACCESS_TOKEN_URL.format(code)
        res_json = wechat_request(url=url, method="GET")
        return res_json["access_token"]

    @classmethod
    def _get_user_info(cls, access_token: str) -> dict:
        url = WECHAT_USER_INFO_URL.format(access_token)
        res_json = wechat_request(url=url, method="GET")
        return res_json
