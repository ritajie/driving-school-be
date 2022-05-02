from car.utils.wechat.message import Message, WechatMessageUtils


class WechatMessageService:
    @classmethod
    def send(cls, message: Message) -> None:
        WechatMessageUtils.send(message)
