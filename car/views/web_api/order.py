import json

from django.db.transaction import atomic
from django.views.generic import View

from car.models import OrderStatus, ServiceError, User
from car.service.order import OrderService
from car.utils.http import http_response


class OrderListView(View):
    def get(self, request):
        with_waitting_coach = bool(int(request.GET.get("with_waitting_coach", "0")))

        if request.user:
            orders = OrderService.get_list(user_id=request.user.id)
        elif request.coach:
            orders = OrderService.get_list(coach_id=request.coach.id)
            if with_waitting_coach:
                order_ids = {order.id for order in orders}
                waitting_coach_orders = OrderService.get_list(
                    status=OrderStatus.WaittingCoach,
                )
                orders += [o for o in waitting_coach_orders if o.id not in order_ids]

        return http_response(
            request=request,
            data=[
                {
                    "id": order.id,
                    "user_id": order.user_id,
                    "status": order.status,
                    "created_at": order.created_at,
                    "last_usage": order.last_usage,
                    "user": {
                        "id": order.user.id,
                        "name": order.user.name,
                    },
                    "coach": {
                        "id": order.coach.id,
                        "name": order.coach.name,
                    }
                    if order.coach
                    else None,
                    "goods": {
                        "id": order.goods.id,
                        "name": order.goods.name,
                        "course_duration": order.goods.course_duration,
                        "origin_price": order.goods.origin_price,
                        "actual_price": order.goods.actual_price,
                        "description": order.goods.description,
                        "car_type": order.goods.car_type,
                        "city": order.goods.city,
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
        # TODO ??????????????????????????????
        # ????????????????????????????????????????????? callback ??????????????????
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
        ???????????? or ??????
        """
        coach = request.coach
        order = OrderService.get_one(order_id)
        body = json.loads(request.body)
        status = OrderStatus(body["status"])

        if coach is None:
            raise ServiceError("??????????????????")
        # NOTE ???????????????????????????????????????
        if status not in (OrderStatus.WaittingCoach, OrderStatus.Serving):
            raise ServiceError("?????????????????????????????????????????????")
        is_acceptting_order = status == OrderStatus.Serving
        is_canceling_order = status == OrderStatus.WaittingCoach
        if is_canceling_order:
            if order.usage_duration != 0:
                raise ServiceError("???????????????????????????????????????????????????????????????????????????????????????")
            if order.coach_id != coach.id:
                raise ServiceError("????????????????????????")
        elif is_acceptting_order:
            if order.coach_id and order.coach_id != coach.id:
                raise ServiceError("???????????????????????????????????????????????????????????????????????????")

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
