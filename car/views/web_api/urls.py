from typing import Any, List

from django.urls import path

from car.views.web_api import (
    api, coach, goods, order, order_usage_record,
    user, wechat_login,
)

urlpatterns: List[Any] = [
    path(
        "users/<int:user_id>",
        user.UserView.as_view(http_method_names=["get", "patch", "post"]),
    ),
    path(
        "orders",
        order.OrderListView.as_view(http_method_names=["get", "post"]),
    ),
    path(
        "orders/<int:order_id>",
        order.OrderOneView.as_view(http_method_names=["patch"]),
    ),
    path(
        "orders/<int:order_id>/usages",
        order_usage_record.OrderUsageListView.as_view(
            http_method_names=["get", "post"],
        ),
    ),
    path(
        "order_usages/<int:order_usage_id>",
        order_usage_record.OrderUsageOneView.as_view(http_method_names=["patch"]),
    ),
    path(
        "goods",
        goods.GoodsView.as_view(http_method_names=["get"]),
    ),
    path(
        "coaches",
        coach.CoachView.as_view(http_method_names=["get", "patch", "post"]),
    ),
    path(
        "wechat_login",
        wechat_login.WechatLoginView.as_view(http_method_names=["post"]),
    ),
    path(
        "",
        api.ApiView.as_view(http_method_names=["get"]),
    ),
]
