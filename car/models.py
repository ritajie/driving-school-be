import enum

from django.db import models


class User(models.Model):
    class Meta:
        db_table = "user"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    email = models.CharField(max_length=255)
    headimg = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Coach(models.Model):
    class Meta:
        db_table = "coach"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    email = models.CharField(max_length=255)
    headimg = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Goods(models.Model):
    class Meta:
        db_table = "goods"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    course_duration = models.IntegerField()
    origin_price = models.IntegerField()
    actual_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderStatus(enum.IntEnum):
    Serving = 0
    Served = 1
    Evaluated = 2


class Order(models.Model):
    class Meta:
        db_table = "order"

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


class OrderUsageRecord(models.Model):
    class Meta:
        db_table = "order_usage_record"

    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    usage_duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
