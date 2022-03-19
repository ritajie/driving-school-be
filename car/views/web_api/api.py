from django.views.generic import View

from car.utils.http import http_response


class ApiView(View):
    def get(self, request):
        return http_response(
            request=request,
            data={
                "id": 1,
                "name": "教练 A",
                "phone": "13800138001",
                "email": "",
                "headimg": "",
            },
        )
