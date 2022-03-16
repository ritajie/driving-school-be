from typing import List, Optional

from car.models import Order, OrderStatus, OrderUsageRecord


class OrderService:
    @classmethod
    def get_list(cls, user_id: int) -> List[Order]:
        return list(Order.objects.filter(user_id=user_id))

    @classmethod
    def get_one(cls, id: int) -> Order:
        return Order.objects.get(id=id)

    @classmethod
    def creat(
        cls,
        user_id: int,
        coach_id: int,
        goods_id: int,
        status: OrderStatus = OrderStatus.Serving,
    ) -> Order:
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
    def get_usage_duration(cls, id: int) -> int:
        return sum(
            OrderUsageRecord.objects.filter(order_id=id).values_list(
                "usage_duration",
                flat=True,
            ),
        )

    @classmethod
    def use(cls, id: int, usage_duration: int) -> None:
        order = cls.get_one(id)
        assert order.status == OrderStatus.Serving, "此订单已经完成服务，不能再生成使用记录"

        has_used_usage_duration = cls.get_usage_duration(id)
        last_usage_duration = order.goods.course_duration - has_used_usage_duration
        assert (
            last_usage_duration >= usage_duration
        ), f"订单剩余量不足，仅剩余 {last_usage_duration} 分钟"

        order_usage_record = OrderUsageRecord(
            order_id=id,
            usage_duration=usage_duration,
        )
        order_usage_record.save()

        if last_usage_duration <= usage_duration:
            order.status = OrderStatus.Served
            order.save()

    @classmethod
    def get_usage_history(cls, id: int) -> List[OrderUsageRecord]:
        return list(OrderUsageRecord.objects.filter(order_id=id))
