import json

from django.db.transaction import atomic
from django.views.generic import View

from car.models import OrderStatus, ServiceError, User
from car.service.order import OrderService
from car.utils.http import http_response


class OrderListView(View):
    def get(self, request):
        orders = OrderService.get_list(user_id=request.user.id)
        return http_response(
            request=request,
            data=[
                {
                    "id": order.id,
                    "user_id": order.user_id,
                    "coach_id": order.coach_id,
                    "goods_id": order.goods_id,
                    "status": order.status,
                    "created_at": order.created_at,
                    "last_usage": order.last_usage,
                    "goods": {
                        "id": order.goods.id,
                        "name": order.goods.name,
                        "course_duration": order.goods.course_duration,
                        "origin_price": order.goods.origin_price,
                        "actual_price": order.goods.actual_price,
                        "description": order.goods.description,
                    },
                    "usage_history": [
                        {
                            "id": usage.id,
                            "order_id": usage.order_id,
                            "usage_duration": usage.usage_duration,
                            "created_at": usage.created_at,
                        }
                        for usage in order.usage_history
                    ],
                }
                for order in orders
            ],
        )

    def post(self, request):
        # TODO 此接口只在测试时使用
        # 未来需要接入支付功能，收到微信 callback 消息后再创建
        user: User = request.user
        body = json.loads(request.body)
        goods_id = body["goods_id"]
        OrderService.create(
            user_id=user.id,
            coach_id=0,
            goods_id=goods_id,
            status=OrderStatus.WaittingCoach,
        )
        return http_response(request=request)


class OrderOneView(View):
    @atomic
    def patch(self, request, order_id: int):
        """
        用于接单 or 退单
        """
        coach = request.coach
        order = OrderService.get_one(order_id)
        body = json.loads(request.body)
        status = OrderStatus(body["status"])

        if coach is None:
            raise ServiceError("没有教练权限")
        # NOTE 此接口只允许教练接单或退单
        if status not in (OrderStatus.WaittingCoach, OrderStatus.Serving):
            raise ServiceError("非法 status")
        is_acceptting_order = status == OrderStatus.Serving
        is_canceling_order = status == OrderStatus.WaittingCoach
        if is_canceling_order:
            if order.usage_duration != 0:
                raise ServiceError("已经有服务记录的订单不允许退单")
            if order.coach_id != coach.id:
                raise ServiceError("您对此订单无权限")
        elif is_acceptting_order:
            if order.coach_id and order.coach_id != coach.id:
                raise ServiceError("此订单已被其他教练接单，请刷新页面查看最新订单状态")

        if is_canceling_order:
            coach_id = 0
        else:
            coach_id = coach.id
        OrderService.update(
            id=order_id,
            coach_id=coach_id,
            status=status,
        )
        return http_response(request=request)
