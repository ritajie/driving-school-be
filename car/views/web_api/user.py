from django.views.generic import View

from car.utils.http import http_response


class UserView(View):
    def get(self, request):
        return http_response(
            request=request,
            data={
                "id": 1,
                "name": "张三",
                "phone": "13800138000",
                "email": "",
                "headimg": "",
            },
        )

    def post(self, request):
        pass

    def patch(self, request):
        pass
