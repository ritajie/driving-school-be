from django.views.generic import View

from car.utils.http import http_response


class OrderListView(View):
    def get(self, request):
        return http_response(
            request=request,
            data=[
                {
                    "id": 1,
                    "user_id": 1,
                    "coach_id": 1,
                    "goods_id": 1,
                    "status": 1,
                },
                {
                    "id": 2,
                    "user_id": 2,
                    "coach_id": 2,
                    "goods_id": 2,
                    "status": 2,
                },
            ],
        )

    def post(self, request):
        return http_response(request=request)


class OrderOneView(View):
    def patch(self, request, order_id: int):
        return http_response(request=request)
