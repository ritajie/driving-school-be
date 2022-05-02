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
        order_id: str,
        course_name: str,
        price: str,
        phone: str,
        created_at: str,
    ) -> None:
        title = "您已成功购买课程"
        data = {
            "first": {
                "value": title,
            },
            "keyword1": {
                "value": order_id,
            },
            "keyword2": {
                "value": course_name,
            },
            "keyword3": {
                "value": price,
            },
            "keyword4": {
                "value": phone,
            },
            "keyword5": {
                "value": created_at,
            },
        }
        super().__init__(
            touser=touser,
            template_id="asD0cVNnVX2szBMUb3BpdSdsp9thPh_zaU8s3etqZWI",
            url="http://car.lulaolu.com/order",
            data=data,
        )


class WechatMessageUtils:
    @classmethod
    def send(cls, message: Message) -> None:
        from .access_token import WechatAccessTokenUtils

        token = WechatAccessTokenUtils.get_one()
        url = SEND_MESSAGE_URL.format(token)
        wechat_request(url=url, method="POST", json=message.to_dict())
