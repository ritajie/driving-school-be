from django.views.generic import View

from car.utils.http import http_response


class UserView(View):
    def get(self, request):
        return http_response(
            request=request,
            data={
                "id": request.user.id,
                "name": request.user.name,
                "phone": request.user.phone,
                "headimg": request.user.headimg,
            },
        )

    def post(self, request):
        pass

    def patch(self, request):
        pass
