from car.service.wechat.send_message import WechatMessageService
from car.utils.wechat.message import CoursePurchasedSuccess

message = CoursePurchasedSuccess(
    touser="ogaHb6jMt9s_kLu8c7k15yh-8WzY",
    order_id="123456789",
    course_name="Python全栈开发",
    price="100元",
    phone="13800138000",
    created_at="2020-01-01 12:00:00",
)
WechatMessageService.send(message)
