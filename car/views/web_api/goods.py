import json

from django.views.generic import View

from car.service.goods import GoodsService
from car.utils.http import http_response


class GoodsView(View):
    def get(self, request):
        goods = GoodsService.get_list()
        return http_response(
            request=request,
            data=[
                {
                    "id": good.id,
                    "name": good.name,
                    "course_duration": good.course_duration,
                    "origin_price": good.origin_price,
                    "actual_price": good.actual_price,
                    "description": good.description,
                }
                for good in goods
            ],
        )

    def post(self, request):
        body = json.loads(request.body)
        name = body["name"]
        course_duration = body["course_duration"]
        origin_price = body["origin_price"]
        actual_price = body["actual_price"]
        description = body.get("description") or ""

        GoodsService.create(
            name=name,
            course_duration=course_duration,
            origin_price=origin_price,
            actual_price=actual_price,
            description=description,
        )

        return http_response(request=request)

    def patch(self, request):
        body = json.loads(request.body)
        id = body["id"]
        name = body.get("name")
        course_duration = body.get("course_duration")
        origin_price = body.get("origin_price")
        actual_price = body.get("actual_price")
        description = body.get("description")

        GoodsService.update(
            id=id,
            name=name,
            course_duration=course_duration,
            origin_price=origin_price,
            actual_price=actual_price,
            description=description,
        )

        return http_response(request=request)
