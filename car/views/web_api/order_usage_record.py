from django.views.generic import View

from car.utils.http import http_response


class OrderUsageListView(View):
    def get(self, request):
        return http_response(
            request=request,
            data=[
                {
                    "id": 1,
                    "order_id": 1,
                    "usage_duration": 1,
                    "created_at": "2020-02-02",
                },
            ],
        )

    def post(self, request):
        return http_response(request=request)


class OrderUsageOneView(View):
    def patch(self, request, order_usage_id: int):
        return http_response(request=request)
