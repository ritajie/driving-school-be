import json

from django.views.generic import View

from car.service.goods import GoodsService
from car.utils.http import http_response


class GoodsView(View):
    def get(self, request):
        # TODO 商品增加 car_type & city 参数过滤
        car_type = request.GET.get("car_type") or None
        city = request.GET.get("city") or None
        goods = GoodsService.get_list(car_type=car_type, city=city)
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
        city = body["city"]
        car_type = body["car_type"]
        description = body.get("description") or ""

        GoodsService.create(
            name=name,
            course_duration=course_duration,
            origin_price=origin_price,
            actual_price=actual_price,
            city=city,
            car_type=car_type,
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
        city = body.get("city")
        car_type = body.get("car_type")
        description = body.get("description")

        GoodsService.update(
            id=id,
            name=name,
            course_duration=course_duration,
            origin_price=origin_price,
            actual_price=actual_price,
            city=city,
            car_type=car_type,
            description=description,
        )

        return http_response(request=request)
