from typing import List, Optional

from car.models import Goods


class GoodsService:
    @classmethod
    def get_list(cls) -> List[Goods]:
        return list(Goods.objects.all())

    @classmethod
    def get_one(cls, id: int) -> Goods:
        return Goods.objects.get(id=id)

    @classmethod
    def exist(cls, id: int) -> bool:
        return Goods.objects.filter(id=id).exists()

    @classmethod
    def create(
        cls,
        name: str,
        course_duration: int,
        origin_price: int,
        actual_price: int,
        description: str = "",
    ) -> Goods:
        goods = Goods(
            name=name,
            course_duration=course_duration,
            origin_price=origin_price,
            actual_price=actual_price,
            description=description,
        )
        goods.save()
        return goods

    @classmethod
    def update(
        cls,
        id: int,
        name: Optional[str] = None,
        course_duration: Optional[int] = None,
        origin_price: Optional[int] = None,
        actual_price: Optional[int] = None,
        description: Optional[str] = None,
    ) -> None:
        goods = Goods.objects.get(id=id)
        if name is not None:
            goods.name = name
        if course_duration is not None:
            goods.course_duration = course_duration
        if origin_price is not None:
            goods.origin_price = origin_price
        if actual_price is not None:
            goods.actual_price = actual_price
        if description is not None:
            goods.description = description
        goods.save()

    @classmethod
    def delete(cls, id: int) -> None:
        Goods.objects.get(id=id).delete()
