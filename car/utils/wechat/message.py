from .base import SEND_MESSAGE_URL, wechat_request


class Message:
    def __init__(
        self,
        touser: str,
        template_id: str,
        url: str,
        data: dict,
    ) -> None:
        self.touser = touser
        self.template_id = template_id
        self.url = url
        self.data = data

    def to_dict(self) -> dict:
        return {
            "touser": self.touser,
            "template_id": self.template_id,
            "url": self.url,
            "data": self.data,
        }


class CoursePurchasedSuccess(Message):
    def __init__(
        self,
        touser: str,
        url: str,
        data: dict,
    ) -> None:
        template_id = "asD0cVNnVX2szBMUb3BpdSdsp9thPh_zaU8s3etqZWI"
        super().__init__(touser, template_id, url, data)


class WechatMessageUtils:
    @classmethod
    def send(cls, message: Message) -> None:
        from .access_token import WechatAccessTokenUtils

        token = WechatAccessTokenUtils.get_one()
        url = SEND_MESSAGE_URL.format(token)
        wechat_request(url=url, method="POST", json=message.to_dict())
