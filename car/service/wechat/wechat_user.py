from car.models import WechatUser
from car.utils.wechat.user import WechatUserUtils


class WechatUserService:
    @classmethod
    def get_one(cls, code: str) -> WechatUser:
        user_info = WechatUserUtils.get_one(code)
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
