import json

from django.views.generic import View

from car.service.order import OrderService
from car.utils.http import http_response


class OrderUsageListView(View):
    def get(self, request, order_id: int):
        order = OrderService.get_one(id=order_id)
        return http_response(
            request=request,
            data=[
                {
                    "id": u.id,
                    "order_id": u.order_id,
                    "usage_duration": u.usage_duration,
                    "created_at": u.created_at,
                }
                for u in order.usage_history
            ],
        )

    def post(self, request, order_id: int):
        body = json.loads(request.body)
        usage_duration = body["usage_duration"]
        assert OrderService.get_one(id=order_id).user_id == request.user.id, "无权限修改此订单"
        OrderService.use(id=order_id, usage_duration=usage_duration)
        return http_response(request=request)


class OrderUsageOneView(View):
    def patch(self, request, order_usage_id: int):
        return http_response(request=request)
