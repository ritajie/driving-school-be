from django.views.generic import View

from car.utils.http import http_response


class UserView(View):
    def get(self, request):
        if request.user:
            data = {
                "id": request.user.id,
                "name": request.user.name,
                "phone": request.user.phone,
                "headimg": request.user.headimg,
                "is_coach": False,
            }
        elif request.coach:
            data = {
                "id": request.coach.id,
                "name": request.coach.name,
                "phone": request.coach.phone,
                "headimg": request.coach.headimg,
                "is_coach": True,
            }
        else:
            data = {}
        return http_response(request=request, data=data)

    def post(self, request):
        pass

    def patch(self, request):
        pass
