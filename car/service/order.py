import datetime
from typing import List, Optional

from car.models import Order, OrderStatus, OrderUsageRecord, ServiceError


class OrderService:
    @classmethod
    def get_list(
        cls,
        user_id: Optional[int] = None,
        coach_id: Optional[int] = None,
        status: Optional[OrderStatus] = None,
    ) -> List[Order]:
        orders = Order.objects.all()
        if user_id is not None:
            orders = orders.filter(user_id=user_id)
        if coach_id is not None:
            orders = orders.filter(coach_id=coach_id)
        if status is not None:
            orders = orders.filter(status=status)
        return list(orders)

    @classmethod
    def get_list_of_coach(cls, coach_id: int) -> List[Order]:
        return list(Order.objects.filter(coach_id=coach_id))

    @classmethod
    def get_one(cls, id: int) -> Order:
        return Order.objects.get(id=id)

    @classmethod
    def create(
        cls,
        user_id: int,
        coach_id: int,
        goods_id: int,
        status: OrderStatus,
    ) -> Order:
        from car.service.goods import GoodsService
        from car.service.user import UserService

        assert UserService.exist(user_id=user_id), "用户不存在"
        assert GoodsService.exist(id=goods_id), "商品不存在"
        # TODO: 校验 coach_id 是否存在

        order = Order(
            user_id=user_id,
            coach_id=coach_id,
            goods_id=goods_id,
            status=status,
        )
        order.save()
        return order

    @classmethod
    def update(
        cls,
        id: int,
        user_id: Optional[int] = None,
        coach_id: Optional[int] = None,
        goods_id: Optional[int] = None,
        status: Optional[OrderStatus] = None,
    ) -> None:
        order = cls.get_one(id)
        if user_id is not None:
            order.user_id = user_id
        if coach_id is not None:
            order.coach_id = coach_id
        if goods_id is not None:
            order.goods_id = goods_id
        if status is not None:
            order.status = status
        order.save()

    @classmethod
    def delete(cls, id: int) -> None:
        cls.get_one(id).delete()

    @classmethod
    def finish_servce(cls, id: int) -> None:
        order = cls.get_one(id)
        order.status = OrderStatus.Served
        order.save()

    @classmethod
    def evaluated(cls, id: int) -> None:
        order = cls.get_one(id)
        order.status = OrderStatus.Evaluated
        order.save()

    @classmethod
    def use(cls, id: int, usage_duration: int, datetime_: datetime.datetime) -> None:
        order = cls.get_one(id)

        if order.status != OrderStatus.Serving:
            raise ServiceError("此订单已经完成服务，不能再生成使用记录")

        last_usage_duration = order.goods.course_duration - order.usage_duration
        if last_usage_duration < usage_duration:
            raise ServiceError(f"订单剩余量不足，仅剩余 {last_usage_duration} 分钟")

        order_usage_record = OrderUsageRecord(
            order_id=id,
            usage_duration=usage_duration,
            datetime=datetime_,
        )
        order_usage_record.save()

        if last_usage_duration <= usage_duration:
            order.status = OrderStatus.Served
            order.save()
