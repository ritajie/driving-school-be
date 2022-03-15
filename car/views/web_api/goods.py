from django.views.generic import View

from car.utils.http import http_response


class GoodsView(View):
    def get(self, request):
        return http_response(
            request=request,
            data=[
                {
                    "id": 1,
                    "name": "订单1",
                    "description": "订单1的描述",
                    "course_duration": 60,
                    "origin_price": 100,
                    "actual_price": 100,
                },
                {
                    "id": 2,
                    "name": "订单2",
                    "description": "订单2的描述",
                    "course_duration": 60,
                    "origin_price": 100,
                    "actual_price": 100,
                },
            ],
        )
