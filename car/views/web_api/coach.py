from django.views.generic import View

from car.utils.http import http_response


class CoachView(View):
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

    def post(self, request):
        pass

    def patch(self, request):
        pass
