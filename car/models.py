import enum
import time
from dataclasses import dataclass
from typing import List, Optional

from django.db import models


class UserType(enum.IntEnum):
    Wechat = 0


class User(models.Model):
    class Meta:
        db_table = "user"
        app_label = "car"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    headimg = models.CharField(max_length=1024)
    platform_openid = models.CharField(max_length=128)
    type = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@dataclass
class WechatUser:
    openid: str
    nickname: str
    sex: int
    language: str
    city: str
    province: str
    country: str
    headimgurl: str
    privilege: List[str]


class Coach(models.Model):
    class Meta:
        db_table = "coach"
        app_label = "car"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    headimg = models.CharField(max_length=1024)
    platform_openid = models.CharField(max_length=128)
    type = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Goods(models.Model):
    class Meta:
        db_table = "goods"
        app_label = "car"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    course_duration = models.IntegerField()
    origin_price = models.IntegerField()
    actual_price = models.IntegerField()
    city = models.CharField(max_length=128)
    car_type = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderStatus(enum.IntEnum):
    WaittingCoach = -1
    Serving = 0
    Served = 1
    Evaluated = 2


class Order(models.Model):
    class Meta:
        db_table = "order"
        app_label = "car"

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    coach_id = models.IntegerField()
    goods_id = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def goods(self) -> Goods:
        return Goods.objects.get(id=self.goods_id)

    @property
    def last_usage(self) -> int:
        return self.goods.course_duration - self.usage_duration

    @property
    def usage_duration(self) -> int:
        return sum(
            OrderUsageRecord.objects.filter(order_id=self.id).values_list(
                "usage_duration",
                flat=True,
            ),
        )

    @property
    def usage_history(self) -> List["OrderUsageRecord"]:
        return list(OrderUsageRecord.objects.filter(order_id=self.id))

    @property
    def user(self) -> User:
        from car.service.user import UserService

        return UserService.get_one(self.user_id)

    @property
    def coach(self) -> Optional[Coach]:
        from car.service.coach import CoachService

        coachs = CoachService.get_list(coach_ids=[self.coach_id])
        return coachs[0] if coachs else None


class OrderUsageRecord(models.Model):
    class Meta:
        db_table = "order_usage_record"
        app_label = "car"

    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    usage_duration = models.IntegerField()
    datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WechatAccessToken(models.Model):
    class Meta:
        db_table = "wechat_access_token"
        app_label = "car"

    access_token = models.CharField(max_length=512)
    expires_in = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def last_expore_seconds(self) -> float:
        return self.created_at.timestamp() + self.expires_in - time.time()


class ServiceError(Exception):
    pass
