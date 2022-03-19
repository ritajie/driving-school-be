import json

from django.views.generic import View

from car.models import User
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
        user: User = request.user
        body = json.loads(request.body)
        coach_id = body["coach_id"]
        goods_id = body["goods_id"]
        OrderService.create(
            user_id=user.id,
            coach_id=coach_id,
            goods_id=goods_id,
        )
        return http_response(request=request)


class OrderOneView(View):
    def patch(self, request, order_id: int):
        return http_response(request=request)
